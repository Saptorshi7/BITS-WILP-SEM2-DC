import socket
import json
import os

# Define the server address and port
server_address = ('172.31.7.156', 12345)
second_server_address = ('172.31.0.252', 12345)  # Address of the second server
buffer_size = 1024
timeout_seconds = 5  # Timeout for connection and response in seconds

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and port
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

hostname = socket.gethostname()

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
            origin = request.get("origin")

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
                    response = {"result": file_content,"server": hostname}
                elif origin < 3:  # Check origin to prevent loop
                    try:
                        # Try connecting to the second server with timeout
                        second_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        second_server_socket.settimeout(timeout_seconds)
                        second_server_socket.connect(second_server_address)

                        # Add origin information to request before sending to second server
                        request["origin"] += 1
                        second_server_socket.sendall(json.dumps(request).encode())

                        # Receive JSON-RPC response from the second server
                        response_data = second_server_socket.recv(buffer_size)
                        response = json.loads(response_data.decode())

                        # Save a copy of the file received from server 2 locally
                        if "result" in response:
                            host = response.get("server")
                            file_content = response["result"]
                            with open(file_name, "wb") as f:
                                f.write(file_content.encode())
                            print(f"File downloaded successfully from '{host}'.")
                    except (ConnectionRefusedError, socket.timeout):
                        # If connection to second server fails or timeout occurs, return file not found
                        response = {"error": "File not found"}

                    finally:
                        second_server_socket.close()
                else:
                    response = {"error": "File not found"}  # Prevent loop by returning error

            else:
                response = {"error": "Method not found"}

            # Send JSON-RPC response to the client
            connection.sendall(json.dumps(response).encode())

    finally:
        # Clean up the connection
        connection.close()

