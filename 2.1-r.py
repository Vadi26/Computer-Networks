# import socket

# SERVER_PORT = 12345

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# server_socket.bind(("localhost", SERVER_PORT))
# print(f"Server listening on {'localhost'}:{SERVER_PORT}")

# def calculate_checksum(message):
#     checksum = 0
#     # Calculate the checksum by XOR-ing all the bytes in the message
#     for byte in message.encode('utf-8'):
#         checksum ^= byte  # Use the integer representation of the byte
#     return checksum

# while True:
#     try:
#         data, client_address = server_socket.recvfrom(1024)
#         if (data.decode('utf-8') == 'exit'):
#             break
#         message, checksum = data.decode('utf-8').split(':', 1)
#         if ':' in checksum:
#             checksum, _ = checksum.split(':', 1)
#         print(message, ':', checksum)

#         if int(checksum) == calculate_checksum(message):
#             packet = "ACK"
#             print(f"Received message: \"{message}\". Sending ACK.")
#             server_socket.sendto(packet.encode(), client_address)

#         else:
#             packet = "NAK"
#             print("Erroneous packet received, sending NAK ...")
#             server_socket.sendto(packet.encode(), client_address)

#         if message.lower() == 'exit':
#             print(f"Connection terminated with {client_address}.")
#             break

#     except KeyboardInterrupt:
#         print(f"Connection interrupted with {client_address}.")

# server_socket.close()


# import socket

# SERVER_PORT = 12345

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# server_socket.bind(("localhost", SERVER_PORT))
# print(f"Server listening on {'localhost'}:{SERVER_PORT}")

# expected_seq = 0

# def calculate_checksum(message):
#     checksum = 0
#     for byte in message.encode('utf-8'):
#         checksum ^= byte
#     return checksum

# while True:
#     try:
#         data, client_address = server_socket.recvfrom(1024)
#         if data.decode('utf-8') == 'exit':
#             break

#         received_message, seqNum, received_checksum = data.decode('utf-8').split(':', 2)

#         seqNum = int(seqNum)
#         received_checksum = int(received_checksum)

#         calculated_checksum = calculate_checksum(received_message)

#         if seqNum == expected_seq and received_checksum == calculated_checksum:
#             packet = f"ACK:{seqNum}"
#             server_socket.sendto(packet.encode(), client_address)
#             print(f"Received message: \"{received_message}\". Sending ACK.")
#             expected_seq = 1 - expected_seq  # Toggle between 0 and 1 for the next expected sequence number.

#         elif seqNum != expected_seq:
#             print(f"Incorrect Sequence Number (Expected {expected_seq}). Sending NAK.")
#             packet = f"NAK:{expected_seq}"
#             server_socket.sendto(packet.encode(), client_address)

#         else:
#             print("Erroneous packet received, sending NAK ...")
#             packet = f"NAK:{expected_seq}"
#             server_socket.sendto(packet.encode(), client_address)

#     except KeyboardInterrupt:
#         print(f"Connection interrupted with {client_address}.")

# server_socket.close()

import socket

SERVER_PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(("localhost", SERVER_PORT))
print(f"Server listening on {'localhost'}:{SERVER_PORT}")

expected_seq = 0

def calculate_checksum(message):
    checksum = 0
    for byte in message.encode('utf-8'):
        checksum ^= byte
    return checksum

while True:
    try:
        data, client_address = server_socket.recvfrom(1024)
        if data.decode('utf-8') == 'exit':
            break

        received_message, seqNum, received_checksum = data.decode('utf-8').split(':', 2)

        seqNum = int(seqNum)
        received_checksum = int(received_checksum)

        calculated_checksum = calculate_checksum(received_message)

        if seqNum == expected_seq and received_checksum == calculated_checksum:
            packet = f"ACK:{seqNum}"
            server_socket.sendto(packet.encode(), client_address)
            print(f"Received message: \"{received_message}\". Sending ACK: {seqNum}")
            expected_seq = 1 - expected_seq  # Toggle between 0 and 1 for the next expected sequence number.

        elif seqNum != expected_seq:
            print(f"Incorrect Sequence Number (Expected {expected_seq}). Sending NAK: {expected_seq}")
            packet = f"NAK:{expected_seq}"
            server_socket.sendto(packet.encode(), client_address)

        else:
            print("Erroneous packet received, sending NAK ...")
            packet = f"NAK:{expected_seq}"
            server_socket.sendto(packet.encode(), client_address)

    except KeyboardInterrupt:
        print(f"Connection interrupted with {client_address}.")

server_socket.close()
