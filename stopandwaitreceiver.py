import socket
import random
import time

# Server configuration
server_host = '127.0.0.1'
server_port = 12345

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
    
