import random

no_of_packets = int(input("Enter the total number of packets: "))
cwnd = 1
last_seq_acked = 0
start_window = 1
threshold = 8

print(f"Initial Threshold = {threshold}")

i = 0
while last_seq_acked != no_of_packets:
    print("\n")

    if i == 10:
        pass

    if (start_window + cwnd - 1) > no_of_packets:
        cwnd = no_of_packets - start_window + 1

    window = list(range(start_window, start_window + cwnd))

    print(f"Sending packets in window: {window}, cwnd = {cwnd}")

    acked_packets = [random.random() <= 0.95 for _ in range(cwnd)]

    lost_packets = [seq for seq, acked in zip(window, acked_packets) if not acked]

    if lost_packets:
        last_seq_acked = lost_packets[0] - 1
        start_window = lost_packets[0]
        threshold = cwnd // 2
        cwnd = 1
        print(f"Packets {lost_packets} lost. Adjusting cwnd and window start.")
        print(f"Resetting cwnd to => {cwnd}")
        print(f"Resetting the Threshold value => {threshold}")
        print(f"Next start window becomes => {start_window}")

    else:
        last_seq_acked = window[-1]
        start_window += cwnd
        if cwnd >= threshold:
            cwnd += 1
        else:
            cwnd *= 2
        print(f"All packets in the window acknowledged. Increasing cwnd and window start.")
        print(f"Increasing cwnd to => {cwnd}")
        print(f"Increasing the start window to => {start_window}")
        print(f"Current Threshold value => {threshold}")

    i += 1
