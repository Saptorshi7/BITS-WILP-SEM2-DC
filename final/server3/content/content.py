import socket
import json
import os
import time

# Define the server address and port
server_address = ('localhost', 12345)
buffer_size = 1024

def generate_files():
    """Generate some example files."""
    files = ["file1.txt", "file2.txt", "file3.txt"]
    for filename in files:
        with open(filename, "w") as f:
            f.write(f"This is {filename} content.")

def upload_file(filename, content):
    """Upload a file to the server."""
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the server
    client_socket.connect(server_address)

    try:
        # Define a JSON-RPC request for uploading the file
        request = {
            "method": "upload",
            "params": {"filename": filename, "content": content}
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
    generate_files()
    print("Files generated.")
    time.sleep(2)  # Wait for the server to be ready

    # Upload each generated file to the server
    for filename in os.listdir():
        if filename.endswith(".txt"):
            with open(filename, "r") as f:
                content = f.read()
                upload_file(filename, content)

