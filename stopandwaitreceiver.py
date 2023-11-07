# import socket
# import random

# # Receiver configuration
# receiver_host = "127.0.0.1"
# receiver_port = 54321

# # Create a UDP socket
# receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# receiver_socket.bind((receiver_host, receiver_port))

# expected_seqNum_num = 0

# while True:
#     packet, addr = receiver_socket.recvfrom(1024)
#     packet_data = packet.decode()
#     seq_num, message = packet_data.split(":", 1)
#     seq_num = int(seq_num)

#     if seq_num == expected_seqNum_num:
#         print(f"Received packet with sequence number {seq_num}: {message}")

#         # Randomly decide whether to send an acknowledgment
#         if random.random() < 0.5:
#             ack = str(seq_num)
#             receiver_socket.sendto(ack.encode(), addr)
#             print(f"Sent acknowledgment for packet {seq_num}")
        
#         expected_seqNum_num = 1 - expected_seqNum_num  # Toggle sequence number
#     else:
#         print(f"Received out-of-order packet. Discarding.")

# receiver_socket.close()

import socket
import random
import hashlib
import time

# Server configuration
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
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_host, server_port))

print(f"Server listening on {server_host}:{server_port}")

expected_seqNum = 0
while True:
    print("-----------")
    data, client_address = server_socket.recvfrom(1024)
    data = data.decode('utf-8')
    data, received_checksum, received_seqNum = data.split(':')
    print("DATA : ", data, "RECEIVED CHECKSUM : ", received_checksum, "RECEIVED SEQNUM : ", received_seqNum)
    # received_seqNum = int(received_seqNum)

    if random.random() < 0.2:
        print("packet lost")
        continue 

    if calculate_checksum(data) == int(received_checksum) and int(expected_seqNum) == int(received_seqNum):
        ack_checksum = calculate_checksum("ACK")
        print(f"Message received: {data} with seq no - {received_seqNum}")
        ACK = f"ACK:{ack_checksum}:{expected_seqNum}"
        time.sleep(2)
        server_socket.sendto(ACK.encode('utf-8'), client_address)
        expected_seqNum +=1
    else:
        print("packet corrupted")
        continue
        #server_socket.sendto(ACK.encode('utf-8'), client_address)
    
