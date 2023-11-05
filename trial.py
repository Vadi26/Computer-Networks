import random
import time
import matplotlib.pyplot as plt

class TCPSlowStart:
    def __init__(self, max_packets=50, drop_probability=0.1, max_congestion_window=16, timeout=5):
        self.max_packets = max_packets
        self.drop_probability = drop_probability
        self.max_congestion_window = max_congestion_window
        self.timeout = timeout
        self.cwnd = 1  # Congestion Window
        self.ssthresh = max_congestion_window // 2
        self.packets_sent = 0
        self.packets_acked = 0
        self.unacked_packets = {}
        self.time_values = []  # Store time values for plotting
        self.cwnd_values = []  # Store cwnd values for plotting
        self.ssthresh_values = []  # Store ssthresh values for plotting
        self.state = "slow_start"  # Current state

    def send_packet(self, packet_num):
        if packet_num <= self.max_packets:
            # Simulate packet transmission
            if random.random() > self.drop_probability:
                return True
        return False

    def receive_ack(self, ack_num):
        if ack_num in self.unacked_packets:
            self.packets_acked += 1
            del self.unacked_packets[ack_num]
            self.cwnd_values.append(self.cwnd)
            self.ssthresh_values.append(self.ssthresh)
            self.time_values.append(time.time() - self.start_time)

            if self.state == "slow_start":
                if self.cwnd < self.ssthresh:
                    self.cwnd += 1
                else:
                    self.state = "congestion_avoidance"
            elif self.state == "congestion_avoidance":
                self.cwnd += int(1 / self.cwnd)

    def timeout_handler(self):
        print("Timeout occurred. Retransmitting packets...")
        self.ssthresh = max(self.cwnd // 2, 2)
        self.cwnd = 1
        self.state = "slow_start"
        for packet_num in self.unacked_packets:
            if packet_num <= self.max_packets:
                self.unacked_packets[packet_num] = time.time()

    def run_simulation(self):
        next_packet_to_send = 1
        self.start_time = time.time()

        while self.packets_acked < self.max_packets:
            for packet_num in range(next_packet_to_send, min(next_packet_to_send + int(self.cwnd), self.max_packets + 1)):
                if self.send_packet(packet_num):
                    self.unacked_packets[packet_num] = time.time()
                    print(f"Sending packet {packet_num} (cwnd={self.cwnd}, ssthresh={self.ssthresh})")

            # Simulate ACK reception
            for packet_num, sent_time in list(self.unacked_packets.items()):
                if packet_num <= self.max_packets:
                    ack_received = random.random() > self.drop_probability
                    if ack_received:
                        ack_num = packet_num
                        print(f"Received ACK for packet {ack_num}")
                        self.receive_ack(ack_num)
                        next_packet_to_send = max(ack_num + 1, next_packet_to_send)
                    elif time.time() - sent_time > self.timeout:
                        self.timeout_handler()
                        next_packet_to_send = min(self.unacked_packets.keys())
                    else:
                        print(f"Packet {packet_num} is unacknowledged (cwnd={self.cwnd}, ssthresh={self.ssthresh})")

            time.sleep(1)

        # Plot the congestion window size and ssthresh over time
        plt.plot(self.time_values, self.cwnd_values, label="cwnd")
        plt.plot(self.time_values, self.ssthresh_values, label="ssthresh")
        plt.xlabel('Time')
        plt.ylabel('Congestion Window Size / ssthresh')
        plt.title('TCP Slow Start and Congestion Avoidance Simulation')
        plt.legend()
        plt.show()

if __name__ == "__main__":
    tcp = TCPSlowStart(max_packets=50, drop_probability=0.1, max_congestion_window=16, timeout=5)
    tcp.run_simulation()
