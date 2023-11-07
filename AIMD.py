import random

def create_window(window_start, cwnd):
    window = list(range(window_start, window_start + cwnd))
    return window

def simulate_acknowledgments(window, cwnd):
    acked_packets = [random.random() <= 0.9 for _ in range(cwnd)]
    return acked_packets

def main():
    n = int(input("Enter the total number of packets: "))
    cwnd = 1
    last_seq_acked = 0
    window_start = 1

    while last_seq_acked < n:
        print("\n")

        if (window_start + cwnd - 1) > n:
            cwnd = n - window_start + 1

        window = list(range(window_start, window_start + cwnd))

        print(f"Sending packets in window: {window}, cwnd = {cwnd}")

        acked_packets = [random.random() <= 0.9 for _ in range(cwnd)]

        lost_packets = [seq for seq, acked in zip(window, acked_packets) if not acked]

        if lost_packets:
            last_seq_acked = lost_packets[0] - 1
            window_start = lost_packets[0]
            cwnd = max(1, cwnd // 2)
            print(f"Packets {lost_packets} lost. Adjusting cwnd and window start.")
            print(f"Resetting cwnd to => {cwnd}")
            print(f"Next start window becomes => {window_start}")
        else:
            last_seq_acked = window[-1]
            window_start += cwnd
            cwnd += 1
            print(f"All packets in the window acknowledged. Increasing cwnd and window start.")
            print(f"Increasing cwnd to => {cwnd}")
            print(f"Increasing the start window to => {window_start}")

main()
