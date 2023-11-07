# import socket
# import time
# import random

# # Sender configuration
# sender_host = "127.0.0.1"
# sender_port = 12345
# receiver_host = "127.0.0.1"
# receiver_port = 54321

# # Create a UDP socket
# sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# window_size = 4
# base = 0
# next_seq_num = 0
# packets = [f"Packet {i}" for i in range(12)]
# acked = [False] * len(packets)

# def send_packets():
#     global next_seq_num, base
#     while next_seq_num < len(packets):
#         if next_seq_num < base + window_size:
#             if random.random() < 0.8:  # Simulating packet loss
#                 packet = f"{next_seq_num}:{packets[next_seq_num]}"
#                 sender_socket.sendto(packet.encode(), (receiver_host, receiver_port))
#                 print(f"Sent packet {next_seq_num}")
#                 if base == next_seq_num:
#                     time.sleep(1)  # Add a delay
#                 next_seq_num += 1
#             else:
#                 print(f"Packet {next_seq_num} dropped (simulated packet loss)")
#                 next_seq_num += 1
#         else:
#             break

# def receive_acks():
#     global next_seq_num, base
#     sender_socket.settimeout(2)  # Set a timeout for acknowledgments
#     try:
#         while True:
#             ack, addr = sender_socket.recvfrom(1024)
#             ack_num = int(ack.decode())
#             print(f"Received acknowledgment for packet {ack_num}")
#             if ack_num == 11:
#                 break
#             if base <= ack_num < base + window_size:
#                 acked[ack_num] = True
#                 while acked[base]:
#                     base += 1
#     except socket.timeout:
#         for i in range(len(acked)):
#             if acked[i] == False:
#                 next_seq_num = i
#                 break
#         send_packets()

# while base < len(packets):
#     send_packets()
#     receive_acks()

# sender_socket.close()

import socket
import random
import hashlib
import time
import threading
# Client configuration
server_host = '127.0.0.1'
server_port = 12345
TIMEOUT = 5
N = 3
base = 0
nxt_seq = 0
sndpkt = []
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


for i in range(100):
    sndpkt.append(0)



def calc_checksum(message):
    hash_obj = hashlib.sha256()
    hash_obj.update(message.encode())
    return hash_obj.hexdigest()


def createpkt(message):
    global nxt_seq
    checksum = calc_checksum(message)
    packet = f"{message}:{checksum}:{nxt_seq}"
    return packet

def rcvpkt():
    global server_port
    global server_host
    global TIMEOUT
    global nxt_seq
    global base
    global N 
    global start_time
    while True:
        data, server_address = client_socket.recvfrom(1024)

        response, rcv_checksum, rcv_seq = data.decode('utf-8').split(":")
        print(f"\nreceived ack with seq number : {rcv_seq}")

        #if random.random() < 0.2:
        #   if random.random() < 0.5:
        #       print("ack lost")
        #       continue
        #   else:
        #       response = "data"

        if calc_checksum(response) == rcv_checksum:

            base = int(rcv_seq) + 1 
            if base == nxt_seq:
            #stop timer here
                start_time = 1e7
                pass
            else:
                start_time = time.time()
        else:
            print("corrupted ack rcvd")
        #we do nothing
            pass



def sendpkt():
    global server_host
    global server_port
    global TIMEOUT
    global N
    global base 
    global nxt_seq
    global sndpkt
    global start_time


    while True:
        message = input(f"window size : {N - nxt_seq+base} Enter your message :")
        packet = createpkt(message)
        if nxt_seq < base + N:
            sndpkt[nxt_seq] = packet
            client_socket.sendto(packet.encode('utf-8'), (server_host, server_port))
            if base == nxt_seq:
                start_time = time.time()
            nxt_seq+=1 
        else:
            print("data refused")

        if TIMEOUT <=  time.time() - start_time:
            print("timeout occurred--------")
            print(f"number of packets to resend = {nxt_seq- base}")
            i= base
            while i < nxt_seq:
                start_time = time.time()
                client_socket.sendto(sndpkt[i].encode('utf-8'), (server_host, server_port))
                i+=1
        else:
            pass


receive_thread = threading.Thread(target=rcvpkt)
receive_thread.start()

send_thread = threading.Thread(target=sendpkt)
send_thread.start()


