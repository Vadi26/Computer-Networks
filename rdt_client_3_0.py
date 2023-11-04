import socket
import hashlib
import random
import time

def cal_checksum(data):
    hash_obj = hashlib.sha256()
    hash_obj.update(data.encode())
    return hash_obj.hexdigest()

SERVER_ADDRESS = ("localhost", 12345)
LOSS_PROBABILITY = 0.75
SEQ_NO = 0
TIMEOUT = 1  

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(TIMEOUT)  

while True:
    try:
        message = input("Client: Enter your message (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break

        checksum = cal_checksum(message)
        old_message = message
        if random.random() > LOSS_PROBABILITY:
            message = "Error"

        packet = f"{message}:{checksum}:{SEQ_NO % 2}"

        if random.random() > LOSS_PROBABILITY:
            packet = f"{message}:{checksum}:{int(not (SEQ_NO % 2))}"

        client_socket.sendto(packet.encode('utf-8'), SERVER_ADDRESS)

        ack_received = False
        start_time = time.time()
        while not ack_received:
            try:
                response, server_addr = client_socket.recvfrom(1024)
                response, checksum, seq_no = response.decode('utf-8').split(":")
                if int(seq_no) != SEQ_NO % 2:
                    print("Received incorrect ACK, waiting for timeout...")

                elif cal_checksum(response) != checksum:
                    print("Received corrupted response, waiting for timeout...")
                    
                else:
                    print("Received ACK")
                    ack_received = True
                    SEQ_NO += 1

            except socket.timeout:
                if time.time() - start_time >= TIMEOUT:
                    print("Timeout occurred. Resending the message...")
                    message = old_message
                    checksum = cal_checksum(message)
                    packet = f"{message}:{checksum}:{SEQ_NO % 2}"
                    client_socket.sendto(packet.encode('utf-8'), SERVER_ADDRESS)

    except Exception as e:
        print(f"Error: {e}")

client_socket.close()
