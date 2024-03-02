import socket

# Define the server address and port
server_address = ('172.31.3.168', 12345)  # Change localhost to the actual IP address of the server
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

    # Receive data from the client
    data = connection.recv(buffer_size)
    print("Received:", data.decode())

finally:
    # Clean up the connection
    connection.close()
    server_socket.close()

