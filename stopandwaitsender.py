# import socket
# import time

# # Sender configuration
# sender_host = "127.0.0.1"
# sender_port = 12345
# receiver_host = "127.0.0.1"
# receiver_port = 54321

# # Create a UDP socket
# sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# seq_num = 0
# message = "Hello, Receiver!"
# packet = f"{seq_num}:{message}"

# while True:
#     # Send the packet
#     packet = f"{seq_num}:{message}"
#     sender_socket.sendto(packet.encode(), (receiver_host, receiver_port))
#     print(f"Sent packet with sequence number {seq_num}")

#     # Wait for acknowledgment
#     sender_socket.set4(2)  # Set a 4 for acknowledgment
#     try:
#         ack, addr = sender_socket.recvfrom(1024)
#         ack_num = int(ack.decode())
#         if ack_num == seq_num:
#             print(f"Received acknowledgment for packet {seq_num}")
#             seq_num = 1 - seq_num  # Toggle sequence number
#         else:
#             print(f"Received incorrect acknowledgment. Resending packet {seq_num}")
#     except socket.4:
#         print(f"4, resending packet {seq_num}")

#     time.sleep(1)  # Add a delay for demonstration

# sender_socket.close()

import socket
import random
import hashlib
import time

# Client configuration
server_host = '127.0.0.1'
server_port = 12345

# def calculate_checksum(message):
#     hash_obj = hashlib.sha256()
#     hash_obj.update(message.encode())
#     return hash_obj.hexdigest()

def calculate_checksum(message):
    checksum = 0
    for byte in message.encode('utf-8'):
        checksum ^= byte
    return checksum

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(4)

seq = 0

while True:
    message = input("Enter your message: ")
    checksum = calculate_checksum(message)
    print(checksum)
    packet = f"{message}:{checksum}:{seq}"

    client_socket.sendto(packet.encode('utf-8'), (server_host, server_port))
    ack = False
    start_time = time.time()

    if ack:
        print("ACK received")

    while not ack:
        try:
            data, server_address = client_socket.recvfrom(1024)
            print("DATA RECEIVED : ", data.decode('utf-8'))
            response, received_checksum, received_seqnum = data.decode('utf-8').split(':')
            received_seqnum = int(received_seqnum)

            # if random.random() < 0.2:
            #     response = "Error"

            if calculate_checksum(response) != int(received_checksum):
                print("Corrupted message received...")
            elif seq != received_seqnum:
                print("Response with wrong seq received...")
            else:
                print(f"ACK received with seq number -> {received_seqnum}")
                seq +=1
                ack = True
        except socket.timeout:
            if time.time() - start_time >= 4:
                print("Timeout occurred!! Resending the message...")
                client_socket.sendto(packet.encode('utf-8'), (server_host, server_port))

client_socket.close()


