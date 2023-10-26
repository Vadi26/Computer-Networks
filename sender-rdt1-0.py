import socket

def sender(message, receiver_host, receiver_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for i, segment in enumerate(message):
        sock.sendto(segment.encode(), (receiver_host, receiver_port))
        print(f"Sent: {segment}")
    sock.close()

while True:
    hehe = input("Send data ? (y/n) ")
    if hehe == 'y':
        msg = input("Enter the message you want to send : ")
        sender([msg], 'localhost', 12345)
    elif hehe == 'n':
        break

# sender(["Segment 1", "Segment 2", "Segment 3"], 'localhost', 12345)