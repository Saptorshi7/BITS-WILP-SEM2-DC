import socket
import json
import os

# Define the server address and port
server_address = ('172.31.15.189', 12345)
second_server_address = ('172.31.13.155', 12345)  # Address of the second server
buffer_size = 1024

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and port
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

print("Waiting for a connection...")

while True:
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
                    # If file not found locally, try downloading from the second server
                    second_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    second_server_socket.connect(second_server_address)
                    try:
                        # Send JSON-RPC request to the second server
                        second_server_socket.sendall(data)
                        # Receive JSON-RPC response from the second server
                        response_data = second_server_socket.recv(buffer_size)
                        response = json.loads(response_data.decode())
                        # Save a copy of the file received from server 2 locally
                        if "result" in response:
                            file_content = response["result"]
                            with open(file_name, "wb") as f:
                                f.write(file_content.encode())
                    finally:
                        second_server_socket.close()
            else:
                response = {"error": "Method not found"}

            # Send JSON-RPC response to the client
            connection.sendall(json.dumps(response).encode())

    finally:
        # Clean up the connection
        connection.close()

