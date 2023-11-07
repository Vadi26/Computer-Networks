import random

def create_window(start_window, cwnd):
    window = list(range(start_window, start_window + cwnd))
    return window

def send_window(window, cwnd):
    print(f"Sending packets in window: {window}, cwnd = {cwnd}")

def simulate_acknowledgments(window, cwnd):
    acked_packets = [random.random() <= 0.95 for _ in range(cwnd)]
    return acked_packets

def main():
    n = int(input("Enter the total number of packets: "))
    cwnd = 1
    last_seq_acked = 0
    start_window = 1
    threshold = 8
    fast_recovery_ack = False

    print(f"Initial Threshold = {threshold}")

    i = 0
    while last_seq_acked != n:
        print("\n")

        if i == 10:
            pass

        if (start_window + cwnd - 1) > n:
            cwnd = n - start_window + 1

        window = list(range(start_window, start_window + cwnd))

        print(f"Sending packets in window: {window}, cwnd = {cwnd}")

        acked_packets = [random.random() <= 0.95 for _ in range(cwnd)]

        if all(acked_packets):
            start_window += cwnd
            if cwnd >= threshold:
                cwnd += 1
            else:
                cwnd *= 2
            last_seq_acked = start_window - 1
            print(f"All packets in the window acknowledged. Increasing cwnd and window start.")
            print(f"Increasing cwnd to => {cwnd}")
            print(f"Increasing the start window to => {start_window}")
            print(f"Current Threshold value => {threshold}")

        else:
            index = acked_packets.index(False)
            lost_packet = window[index]
            last_seq_acked = lost_packet - 1
            start_window = lost_packet
            threshold = cwnd // 2

            print("Some packet loss / error occured !")
            print(f"Resetting cwnd to => {cwnd}")
            print(f"Resetting the Threshold value => {threshold}")
            print(f"Next start window becomes => {start_window}")

            fast_recovery_ack = False
            print("\n-----------------Starting fast recovery-----------------\n")

            cwnd = threshold + 3
            if (start_window + cwnd - 1) > n:
                cwnd = n - start_window + 1

            while not fast_recovery_ack:
                window = create_window(start_window, cwnd)
                send_window(window, cwnd)
                acked_packets = simulate_acknowledgments(window, cwnd)

                if all(acked_packets[:3]):
                    fast_recovery_ack = True
                    cwnd = 1
                    start_window = lost_packet
                    print("\n-----------------Ending fast recovery-----------------\n")
                else:
                    print("Resending window until 3 duplicate ACKs are not received...")
            continue


main()
