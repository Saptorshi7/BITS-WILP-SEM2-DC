import socket
import json

# Define the server address and port
server_address = ('localhost', 12345)
buffer_size = 1024

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server
client_socket.connect(server_address)

try:
    # Define a JSON-RPC request
    request = {
        "method": "echo",
        "params": "Hello, server!"
    }

    # Send JSON-RPC request to the server
    client_socket.sendall(json.dumps(request).encode())

    # Receive JSON-RPC response from the server
    data = client_socket.recv(buffer_size)

    # Decode JSON data
    response = json.loads(data.decode())
    result = response.get("result")
    error = response.get("error")

    # Print the result or error message
    if result:
        print("Received:", result)
    elif error:
        print("Error:", error)

finally:
    # Clean up the connection
    client_socket.close()

