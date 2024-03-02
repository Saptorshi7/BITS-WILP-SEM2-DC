import socket

# Define the server address and port
server_address = ('172.31.3.168', 12345)  # Change localhost to the actual IP address of the server
buffer_size = 1024

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server
client_socket.connect(server_address)

try:
    # Send data to the server
    message = "Hello, server!"
    print("Sending:", message)
    client_socket.sendall(message.encode())

    # Receive response from the server
    data = client_socket.recv(buffer_size)
    print("Received:", data.decode())

finally:
    # Clean up the connection
    client_socket.close()

