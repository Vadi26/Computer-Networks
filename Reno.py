import matplotlib.pyplot as plt
import random

class TCPRenoAlternative:
    def __init__(self, max_packets, initial_threshold, timeouts, dupacks, threedupacks):
        self.max_packets = max_packets
        self.initial_threshold = initial_threshold
        self.timeouts = timeouts
        self.dupacks = dupacks
        self.threedupacks = threedupacks
        self.x_data = []
        self.y_data = []
        self.base_cwnd = 1
        self.ss_phase = 1
        self.ca_phase = 0
        self.fr_phase = 0
        self.current_cwnd = 1
        self.dupack_count = 0

    def simulate(self):
        for i in range(1, self.max_packets + 1):
            if i == 1:
                self.current_cwnd = self.base_cwnd
            else:
                if i in self.timeouts:
                    if self.ca_phase == 1:
                        self.ca_phase = 0
                    if self.fr_phase == 1:
                        self.fr_phase = 0
                    self.ss_phase = 1
                    self.current_cwnd = self.base_cwnd
                    self.dupack_count = 0
                elif i - 1 in self.dupacks:
                    if self.ss_phase == 1:
                        self.ss_phase = 0
                        self.dupack_count += 1
                        self.current_cwnd *= 2
                    elif self.ca_phase == 1:
                        self.ca_phase = 0
                        self.dupack_count += 1
                    else:
                        self.current_cwnd = self.current_cwnd + 1
                elif i - 1 in self.threedupacks:
                    if self.ss_phase == 1:
                        self.ss_phase = 0
                    elif self.ca_phase == 1:
                        self.ca_phase = 0
                    self.fr_phase = 1
                    ssthresh = int(self.current_cwnd / 2)
                    self.current_cwnd = ssthresh + 3
                else:
                    if self.ss_phase == 1:
                        self.current_cwnd *= 2
                    elif self.ca_phase == 1:
                        self.current_cwnd += 1
                    else:
                        ssthresh = int(self.current_cwnd / 2)
                        self.current_cwnd = ssthresh
                        self.fr_phase = 0
                        self.ca_phase = 1
                    self.dupack_count = 0

            self.x_data.append(i)
            self.y_data.append(self.current_cwnd)

    def plot_results(self):
        fig = plt.figure(figsize=(9, 7), facecolor="#b5b0bf")
        ax = plt.axes()
        ax.set_facecolor("#b5b0bf")

        plt.xticks(self.x_data)
        right_side = ax.spines["right"]
        right_side.set_visible(False)
        top_line = ax.spines["top"]
        top_line.set_visible(False)

        fontsize = 15
        ax.plot(self.x_data, self.y_data, marker=".", color="#513f8f", linewidth=2, markerfacecolor="black", markersize=12)
        plt.title("Alternative TCP Reno Simulation", fontdict={'fontsize': fontsize + 5})
        plt.xlabel("Packets sent (RTTs)", fontdict={'fontsize': fontsize})
        plt.ylabel("Size of cwnd (in MSS)", fontdict={'fontsize': fontsize})
        plt.grid(True, color='#b5b0bf', linestyle='-', linewidth=2)
        plt.gca().patch.set_facecolor('0.8')
        plt.show()

if __name__ == "__main__":
    max_packets = int(input("Enter the number of packets to be sent: "))
    initial_threshold = int(input("Enter the initial threshold: "))
    timeouts = [int(x) for x in input("Enter at what packets the timeout occurs with spaces in between: ").split()]
    dupacks = [int(x) for x in input("Enter at what packets duplicate ACKs arrive with spaces in between: ").split()]
    threedupacks = [int(x) for x in input("Enter at what packets 3 duplicate ACKs arrive with spaces in between: ").split()]

    simulation = TCPRenoAlternative(max_packets, initial_threshold, timeouts, dupacks, threedupacks)
    simulation.simulate()
    simulation.plot_results()
