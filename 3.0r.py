# import socket
# import time

# SERVER_PORT = 12345
# SEQ_NUM = 0

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# server_socket.bind(("localhost", SERVER_PORT))
# print(f"Server listening on {'localhost'}:{SERVER_PORT}")
# expectedSeq = 1

# def calculate_checksum(message):
#     checksum = 0
#     # Calculate the checksum by XOR-ing all the bytes in the message
#     for byte in message.encode('utf-8'):
#         checksum ^= byte  # Use the integer representation of the byte
#     return checksum

# while True:
#     # try:
#         prev = SEQ_NUM
#         data, client_address = server_socket.recvfrom(1024)
#         if (data.decode('utf-8') == 'exit'):
#             break
#         message, rest = data.decode('utf-8').split(':', 1)
#         checksum, seqNum = rest.split(':', 1)
#         if ':' in checksum:
#             checksum, _ = checksum.split(':', 1)

#         if checksum == str(calculate_checksum(message)) and seqNum == SEQ_NUM:
#             SEQ_NUM = SEQ_NUM ^ 1
#             sendingChecksum = calculate_checksum("ACK")
#             packet = "ACK" + ':' + sendingChecksum + ':' + str(SEQ_NUM)
#             print(f"Received message ->  \"{message}\".")
#             print("Rsponse being sent -> ", packet)
#             server_socket.sendto(packet.encode(), client_address)

#         if ':' in seqNum:
#             seqNum, _ = seqNum.split(':', 1)

#         if int(seqNum) != SEQ_NUM:
#             print("Incorrect sequence number")
#             time.sleep(2)

#         if message.lower() == 'exit':
#             print(f"Connection terminated with {client_address}.")
#             break

#     # except KeyboardInterrupt:
#     #     print(f"Connection interrupted with {client_address}.")

# server_socket.close()


import socket
import time

SERVER_PORT = 12345
SEQ_NUM = 0

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(("localhost", SERVER_PORT))
print(f"Server listening on {'localhost'}:{SERVER_PORT}")
expectedSeq = 1

def calculate_checksum(message):
    checksum = 0
    for byte in message.encode('utf-8'):
        checksum ^= byte
    return checksum

while True:
    try:
        data, client_address = server_socket.recvfrom(1024)
        if (data.decode('utf-8') == 'exit'):
            break
        message, rest = data.decode('utf-8').split(':', 1)
        checksum, seqNum = rest.split(':', 1)
        if ':' in checksum:
            checksum, _ = checksum.split(':', 1)

        if int(seqNum) == SEQ_NUM and checksum == str(calculate_checksum(message)):
            SEQ_NUM = 1 - SEQ_NUM
            sendingChecksum = calculate_checksum("ACK")
            packet = "ACK" + ':' + str(sendingChecksum) + ':' + str(SEQ_NUM)
            print(f"Received message ->  \"{message}\".")
            print("Response being sent -> ", packet)
            server_socket.sendto(packet.encode(), client_address)

        elif int(seqNum) != SEQ_NUM:
            print("Incorrect sequence number")
            time.sleep(2)

        if message.lower() == 'exit':
            print(f"Connection terminated with {client_address}.")
            break

    except KeyboardInterrupt:
        print(f"Connection interrupted with {client_address}.")

server_socket.close()
