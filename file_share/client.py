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
    # Prompt the user to enter the filename to download
    filename = input("Enter the filename to download: ")

    # Define a JSON-RPC request for downloading the specified file
    request = {
        "method": "download",
        "params": {"filename": filename}
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
        print("Received file content:")
        print(result)
    elif error:
        print("Error:", error)

finally:
    # Clean up the connection
    client_socket.close()

