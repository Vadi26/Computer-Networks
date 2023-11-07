import socket
import random

# Receiver configuration
receiver_host = "127.0.0.1"
receiver_port = 54321

# Create a UDP socket
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket.bind((receiver_host, receiver_port))

# ith index willl be True if the acknowledgement of the packet with that sequence number is lost
ack_lost = [False] * 12

expected_seq_num = 0

def send_acknowledgment(seq_num, addr):
    if random.random() < 0.2:  # Simulate acknowledgment loss with 20% probability
        print(f"Acknowledgment for packet {seq_num} is lost.")
        ack_lost[seq_num] = True
    else:
        ack = str(seq_num)
        receiver_socket.sendto(ack.encode(), addr)
        print(f"Sent acknowledgment for packet {seq_num}")

while expected_seq_num < 12:
    packet, addr = receiver_socket.recvfrom(1024)
    packet_data = packet.decode()
    seq_num, message = packet_data.split(":", 1)
    seq_num = int(seq_num)

    if expected_seq_num <= seq_num < expected_seq_num + 4 or ack_lost[seq_num] == True:
        print(f"Received packet with sequence number {seq_num}: {message}")
        send_acknowledgment(seq_num, addr)
        expected_seq_num = seq_num + 1
    else:
        print(f"Received out-of-order packet {seq_num}. Discarding.")

receiver_socket.close()

# import socket
# import random
# import hashlib
# import time

# # Server configuration
# server_host = '127.0.0.1'
# server_port = 12345

# def calc_checksum(message):
#     hash_obj = hashlib.sha256()
#     hash_obj.update(message.encode())
#     return hash_obj.hexdigest()

# # Create a socket
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_socket.bind((server_host, server_port))

# print(f"Server listening on {server_host}:{server_port}")

# expected_seq = 0
# while True:
#     print("Receiving packet-----------")
#     data, client_address = server_socket.recvfrom(1024)
#     data = data.decode('utf-8')
#     data, rcv_checksum, rcv_seq = data.split(':')
#     rcv_seq = int(rcv_seq)

#     if random.random() < 0.2:
#         if random.random() < 0.8:
#             print("packet lost")
#             continue
#         else:
#             data = "error"   

#     if calc_checksum(data) == rcv_checksum and expected_seq == rcv_seq:
#         ack_checksum = calc_checksum("ACK")
#         print(f"Message received: {data} with seq no - {rcv_seq}")
#         ACK = f"ACK:{ack_checksum}:{expected_seq}"
#         time.sleep(3)
#         server_socket.sendto(ACK.encode('utf-8'), client_address)
#         expected_seq +=1
#     else:
#         print("packet corrupted")
#         continue
#         #server_socket.sendto(ACK.encode('utf-8'), client_address)
    