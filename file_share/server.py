import socket
import json
import os

# Define the server address and port
server_address = ('localhost', 12345)
buffer_size = 1024

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and port
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

print("Waiting for a connection...")

# Accept a connection
connection, client_address = server_socket.accept()

try:
    print("Connection established with", client_address)

    while True:
        # Receive JSON-RPC request from the client
        data = connection.recv(buffer_size)
        if not data:
            break

        # Decode JSON data
        request = json.loads(data.decode())
        method = request.get("method")
        params = request.get("params")

        # Process the RPC request
        if method == "upload":
            file_content = params.get("content")
            file_name = params.get("filename")
            with open(file_name, "wb") as f:
                f.write(file_content.encode())
            response = {"result": "File uploaded successfully"}
        elif method == "download":
            file_name = params.get("filename")
            if os.path.exists(file_name):
                with open(file_name, "rb") as f:
                    file_content = f.read().decode()
                response = {"result": file_content}
            else:
                response = {"error": "File not found"}
        else:
            response = {"error": "Method not found"}

        # Send JSON-RPC response to the client
        connection.sendall(json.dumps(response).encode())

finally:
    # Clean up the connection
    connection.close()
    server_socket.close()

