import random

def create_window(window_start, cwnd):
    window = [] * cwnd
    window_acks = [] * cwnd
    for i in range(0, cwnd):
        window.append(window_start + i)
        window_acks.append(False)
    return window, window_acks

def send_window(window, cwnd):
    print(f"send window: {window}, cwnd = {cwnd}")

def get_ack(window, window_acks, cwnd):
    for i in range(0, cwnd):
        if random.random() <= 0.95:
            window_acks[i] = True
            print(f"        ACK {window[i]} arrived")
    return window_acks

def main():
    n = int(input("Enter number of packets: "))
    cwnd = 1
    last_seq_acked = 0
    window_start = 1
    window = []
    window_acks = []
    threshold = 8
    fast_recovery_ack = False

    print(f"Initial Threshold = {threshold}")
    
    i = 0
    while last_seq_acked != n:
        print("\n")
        if i == 10:
            #break
            pass

        if(window_start + cwnd - 1) > n:
            cwnd = n - window_start + 1
        window, window_acks = create_window(window_start, cwnd)

        send_window(window, cwnd)

        window_acks = get_ack(window, window_acks, cwnd)

        if all(window_acks):
            window_start += cwnd
            if(cwnd >= threshold):
                cwnd +=1
            else:
                cwnd *= 2
            last_seq_acked = window_start - 1
            print(f"New congestion window = {cwnd}")
            print(f"New window start = {window_start}")

        else:
            index = window_acks.index(False)
            lost_packet = window[index]
            last_seq_acked = lost_packet - 1
            window_start = lost_packet
            threshold = cwnd // 2

            print(f"New congestion window = {cwnd}")
            print(f"New Threshold = {threshold}")
            print(f"New window start = {window_start}")

            fast_recovery_ack = False
            print("\nStarting fast recovery\n")

            cwnd = threshold + 3
            if(window_start + cwnd - 1) > n:
                cwnd = n - window_start + 1

            while(not fast_recovery_ack):

                window, window_acks = create_window(window_start, cwnd)
                send_window(window, cwnd)
                window_acks = get_ack(window, window_acks, cwnd)
                #print(f"window_acks = {window_acks}")

                if all(window_acks[:3]):
                #if last_seq_acked >= window_start + 2:
                    #print(window_start[0:4])
                    fast_recovery_ack = True
                    cwnd = 1
                    window_start = lost_packet
                    print("\nEnding fast recovery\n")
                    
                else:
                    print("resending window till 3 duplicate ACK not revieved...")
                    #index = window_acks.index(False)
                    #lost_packet = window[index]
                    #last_seq_acked = lost_packet - 1


            continue

        i +=1





if __name__ == "__main__":
    main()
