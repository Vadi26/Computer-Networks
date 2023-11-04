# import socket
# import time
# import random
# import copy

# SERVER_ADDRESS = ("localhost", 12345)
# SEQ_NUM = 0
# TIMEOUT = 1 

# client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# client_socket.settimeout(TIMEOUT) 

# def calculate_checksum(message):
#     checksum = 0

#     # Calculate the checksum by XOR-ing all the bytes in the message
#     for byte in message.encode('utf-8'):
#         checksum ^= byte  # Use the integer representation of the byte

#     return checksum

# while True:
#     try:
#         message = input("Client: Enter your message (or 'exit' to quit): ")
#         SEQ_NUM = SEQ_NUM ^ 1
#         if message.lower() == 'exit':
#             packet = message.encode('utf-8')
#             client_socket.sendto(packet, SERVER_ADDRESS)
#             break
        
#         originalMessage = copy.deepcopy(message)
#         checksum = calculate_checksum(message)
#         message = message + ':' + str(checksum) + ':' + str(SEQ_NUM)
#         originalMessage = originalMessage + ':' + str(checksum) + ':' + str(SEQ_NUM)
        
#         if random.random() < 0.5:
#             error_position = random.randint(0, len(message) - 4)
#             message = message[:error_position] + chr(ord(message[error_position]) ^ 1) + message[error_position + 1:]

#         # packet = message + ":" + bytes(checksum)
#         packet = message.encode('utf-8')

#         client_socket.sendto(packet, SERVER_ADDRESS)

#         ack_received = False
#         startTime = time.time()
#         while not ack_received:
#             try:
#                 response, server_addr = client_socket.recvfrom(1024)
#                 response, checksum, seq_no = response.decode('utf-8').split(":")
#                 if int(seq_no) != SEQ_NUM % 2:
#                     print("Received incorrect ACK, waiting for timeout...")

#                 elif calculate_checksum(response) != checksum:
#                     print("Received corrupted response, waiting for timeout...")
                    
#                 else:
#                     print("Received ACK")
#                     ack_received = True
#                     SEQ_NUM += 1

#             except socket.timeout:
#                 if time.time() - startTime >= TIMEOUT:
#                     print("Timeout occurred. Resending the message...")
#                     message = originalMessage
#                     checksum = calculate_checksum(message)
#                     packet = f"{message}:{checksum}:{SEQ_NUM % 2}"
#                     client_socket.sendto(packet.encode('utf-8'), SERVER_ADDRESS)
#         # ackNAK, _ = client_socket.recvfrom(5)
#         # ack, seqNum = ackNAK.decode('utf-8').split(':', 1)
#         # if seqNum == str(SEQ_NUM):
#         #     print(f"ACK {SEQ_NUM} received ")
#         # else:
#         #     while int(seqNum) != SEQ_NUM:
#         #         print(f"ACK {seqNum} received")
#         #         print("Received ACK number : ", seqNum, "Expected ACK number : ", SEQ_NUM)
#         #         print("Resending the packet ...")
#         #         time.sleep(2)
#         #         checksum = calculate_checksum(originalMessage)
#         #         message = originalMessage + ':' + str(checksum) + ':' + str(SEQ_NUM)

#         #         if random.random() < 0.1:
#         #             error_position = random.randint(0, len(message) - 4)
#         #             message = message[:error_position] + chr(ord(message[error_position]) ^ 1) + message[error_position + 1:]

#         #         packet = message.encode('utf-8')
#         #         client_socket.sendto(packet, SERVER_ADDRESS)
#         #         time.sleep(2)
#         #         ackNAK, _ = client_socket.recvfrom(5)
#         #         ack, seqNum = ackNAK.decode('utf-8').split(':', 1)

#     except Exception as e:
#         print(f"Error: {e}")

# client_socket.close()

import socket
import time
import random
import copy

SERVER_ADDRESS = ("localhost", 12345)
SEQ_NUM = 0
TIMEOUT = 1 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(TIMEOUT)

def calculate_checksum(message):
    checksum = 0
    for byte in message.encode('utf-8'):
        checksum ^= byte
    return checksum

while True:
    try:
        message = input("Client: Enter your message (or 'exit' to quit): ")
        SEQ_NUM = 1 - SEQ_NUM
        if message.lower() == 'exit':
            packet = message.encode('utf-8')
            client_socket.sendto(packet, SERVER_ADDRESS)
            break
        
        originalMessage = copy.deepcopy(message)
        checksum = calculate_checksum(message)
        message = message + ':' + str(checksum) + ':' + str(SEQ_NUM)
        originalMessage = originalMessage + ':' + str(checksum) + ':' + str(SEQ_NUM)
        
        if random.random() < 0.5:
            error_position = random.randint(0, len(message) - 4)
            message = message[:error_position] + chr(ord(message[error_position]) ^ 1) + message[error_position + 1:]

        packet = message.encode('utf-8')
        client_socket.sendto(packet, SERVER_ADDRESS)
        print(f"Sent message: \"{originalMessage}\" with SEQ: {SEQ_NUM} and Checksum: {checksum}")

        ack_received = False
        startTime = time.time()
        while not ack_received:
            try:
                response, server_addr = client_socket.recvfrom(1024)
                response, checksum, seq_no = response.decode('utf-8').split(":")
                if int(seq_no) != SEQ_NUM:
                    print("Received incorrect ACK, waiting for timeout...")
                    continue

                if calculate_checksum(response) != int(checksum):
                    print("Received corrupted response, waiting for timeout...")
                    continue

                print(f"Received ACK for SEQ: {SEQ_NUM}")
                ack_received = True
            except socket.timeout:
                if time.time() - startTime >= TIMEOUT:
                    print("Timeout occurred. Resending the message...")
                    message = originalMessage
                    checksum = calculate_checksum(message)
                    packet = f"{message}:{checksum}:{SEQ_NUM}"
                    client_socket.sendto(packet.encode('utf-8'), SERVER_ADDRESS)
        # ackNAK, _ = client_socket.recvfrom(5)
        # ack, seqNum = ackNAK.decode('utf-8').split(':', 1)
        # if seqNum == str(SEQ_NUM):
        #     print(f"ACK {SEQ_NUM} received ")
        # else:
        #     while int(seqNum) != SEQ_NUM:
        #         print(f"ACK {seqNum} received")
        #         print("Received ACK number : ", seqNum, "Expected ACK number : ", SEQ_NUM)
        #         print("Resending the packet ...")
        #         time.sleep(2)
        #         checksum = calculate_checksum(originalMessage)
        #         message = originalMessage + ':' + str(checksum) + ':' + str(SEQ_NUM)

        #         if random.random() < 0.1:
        #             error_position = random.randint(0, len(message) - 4)
        #             message = message[:error_position] + chr(ord(message[error_position]) ^ 1) + message[error_position + 1:]

        #         packet = message.encode('utf-8')
        #         client_socket.sendto(packet, SERVER_ADDRESS)
        #         time.sleep(2)
        #         ackNAK, _ = client_socket.recvfrom(5)
        #         ack, seqNum = ackNAK.decode('utf-8').split(':', 1)

    except Exception as e:
        print(f"Error: {e}")

client_socket.close()
