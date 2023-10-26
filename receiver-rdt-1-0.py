import socket

def receiver(receiver_host, receiver_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((receiver_host, receiver_port))
    while True:
        data, addr = sock.recvfrom(1024)
        if not data:
            break
        print(f"Received: {data.decode()}")

receiver('localhost', 12345)
