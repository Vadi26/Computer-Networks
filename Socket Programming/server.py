import socket

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    # '5' indicates that it allows upto 5 pending connections in the servers connection queue
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Handle client communication
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                print(f"Connection closed with {client_address}")
                break

            print(f"Received from client: {data}")

            # Echo the received message back to the client
            response = input("Enter your reply: ")
            client_socket.send(response.encode('utf-8'))

        client_socket.close()


host = "0.0.0.0"  # Replace with your server's IP
port = 12344  # Choose an available port
start_server(host, port)
