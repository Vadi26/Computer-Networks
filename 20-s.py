import socket
import time
import random
import copy

SERVER_ADDRESS = ("localhost", 12345)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def calculate_checksum(message):
    checksum = 0

    # Calculate the checksum by XOR-ing all the bytes in the message
    for byte in message.encode('utf-8'):
        checksum ^= byte  # Use the integer representation of the byte

    return checksum

while True:
    try:
        message = input("Client: Enter your message (or 'exit' to quit): ")
        if message.lower() == 'exit':
            packet = message.encode('utf-8')
            client_socket.sendto(packet, SERVER_ADDRESS)
            break
        
        originalMessage = copy.deepcopy(message)
        checksum = calculate_checksum(message)
        message = message + ':' + str(checksum)
        originalMessage = originalMessage + ':' + str(checksum)
        # Simulate random errors (50% chance of introducing an error)
        if random.random() < 0.5:
            # Introduce an error by flipping a random bit in the packet
            error_position = random.randint(0, len(message) - 4)
            message = message[:error_position] + chr(ord(message[error_position]) ^ 1) + message[error_position + 1:]
            # message = message.encode()

        # packet = message + ":" + bytes(checksum)
        packet = message.encode('utf-8')

        client_socket.sendto(packet, SERVER_ADDRESS)

        ack_received = False
        ackNAK, _ = client_socket.recvfrom(5)
        ackNAK = ackNAK.decode()
        if ackNAK == "ACK":
            print("ACK received !")
        else:
            while ackNAK != "ACK":
                print("NAK received. Resending...")
                time.sleep(2)
                checksum = calculate_checksum(originalMessage)
                message = originalMessage + ':' + str(checksum)
                # Simulate random errors (50% chance of introducing an error)
                if random.random() < 0.1:
                    # Introduce an error by flipping a random bit in the packet
                    error_position = random.randint(0, len(message) - 4)
                    message = message[:error_position] + chr(ord(message[error_position]) ^ 1) + message[error_position + 1:]
                    # message = message.encode()

                # packet = message + ":" + bytes(checksum)
                packet = message.encode('utf-8')
                client_socket.sendto(packet, SERVER_ADDRESS)
                ackNAK, _ = client_socket.recvfrom(5)
                print("AKCNAK", ackNAK)
                ackNAK = ackNAK.decode()

    except Exception as e:
        print(f"Error: {e}")

client_socket.close()

