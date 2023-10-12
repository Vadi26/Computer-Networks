import socket

def start_client(server_host, server_port):
    # used socket.SOCK_STREAM for TCP connection
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # to establish connection to the server
    client_socket.connect((server_host, server_port))

    while True:
        message = input("Enter your message to the server (type 'exit' to quit): ")
        if message.lower() == 'exit':
            break

        # send the message to the server
        client_socket.send(message.encode('utf-8'))

        # receive and print the server's response
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Received from server: {response}")

    # this line releases the resources and properly closes the connection
    print("Closing the connection !")
    client_socket.close()

server_host = "0.0.0.0"  # Replace with the server's IP
server_port = 12344  # Use the same port as the server
start_client(server_host, server_port)
