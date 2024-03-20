import socket
import json
import os

# Define the server address and port
server_address = ('172.31.2.52', 12345)
buffer_size = 1024

def transmit_files(directory):
    """Transmit files from the specified directory to the server."""
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the server
    client_socket.connect(server_address)

    try:
        # Iterate over files in the specified directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                with open(file_path, "rb") as f:
                    file_content = f.read()

                # Define a JSON-RPC request for uploading the file
                request = {
                    "method": "upload",
                    "params": {"filename": filename, "content": file_content.decode()}
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
                    print(f"File '{filename}' uploaded successfully.")
                elif error:
                    print("Error:", error)

    finally:
        # Clean up the connection
        client_socket.close()

if __name__ == "__main__":
    # Specify the directory containing the files to transmit
    directory = "files_to_transmit"

    # Transmit files from the specified directory to the server
    transmit_files(directory)
