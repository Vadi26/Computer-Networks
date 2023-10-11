import socket

def start_client(server_host, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    while True:
        message = input("Enter your message to the server (type 'exit' to quit): ")
        if message.lower() == 'exit':
            break

        # Send the message to the server
        client_socket.send(message.encode('utf-8'))

        # Receive and print the server's response
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Received from server: {response}")

    client_socket.close()

if __name__ == "__main__":
    server_host = "127.0.0.1"  # Replace with the server's IP
    server_port = 12345  # Use the same port as the server
    start_client(server_host, server_port)
