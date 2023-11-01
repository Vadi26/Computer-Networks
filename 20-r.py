import socket

SERVER_PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(("localhost", SERVER_PORT))
print(f"Server listening on {'localhost'}:{SERVER_PORT}")

def calculate_checksum(message):
    checksum = 0
    # Calculate the checksum by XOR-ing all the bytes in the message
    for byte in message.encode('utf-8'):
        checksum ^= byte  # Use the integer representation of the byte
    return checksum

while True:
    try:
        data, client_address = server_socket.recvfrom(1024)
        if (data.decode('utf-8') == 'exit'):
            break
        message, checksum = data.decode('utf-8').split(':', 1)
        if ':' in checksum:
            checksum, _ = checksum.split(':', 1)
        print(message, ':', checksum)

        if int(checksum) == calculate_checksum(message):
            packet = "ACK"
            print(f"Received message: \"{message}\". Sending ACK.")
            server_socket.sendto(packet.encode(), client_address)

        else:
            packet = "NAK"
            print("Erroneous packet received, sending NAK ...")
            server_socket.sendto(packet.encode(), client_address)

        if message.lower() == 'exit':
            print(f"Connection terminated with {client_address}.")
            break

    except KeyboardInterrupt:
        print(f"Connection interrupted with {client_address}.")

server_socket.close()
