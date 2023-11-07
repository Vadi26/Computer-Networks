import matplotlib.pyplot as plt
import random

class TCPSlowStartSimulation:
    def __init__(self, max_packets, ssthresh):
        self.max_packets = max_packets
        self.ssthresh = ssthresh
        self.xValues = []
        self.yValues = []
        self.initial_cwnd = 1
        self.isThresh = 1
        self.isCongestionAvoidance = 0
        self.current_cwnd = 1
        # Generate at least 3 timeouts
        self.timeout_packets = sorted(random.sample(range(1, max_packets + 1), max(3, random.randint(1, max_packets))))

    def run_simulation(self):
        i = 1
        timeout_index = 0
        while i <= self.max_packets:
            self.xValues.append(i)
            if i == 1:
                self.current_cwnd = self.initial_cwnd
            else:
                if timeout_index < len(self.timeout_packets) and i == self.timeout_packets[timeout_index]:
                    if self.isThresh:
                        self.current_cwnd *= 2
                    else:
                        self.current_cwnd += 1
                    self.isThresh = 1
                    self.isCongestionAvoidance = 0
                    self.xValues.append(i)
                    self.yValues.append(self.current_cwnd)
                    self.ssthresh = int(self.current_cwnd / 2)
                    self.current_cwnd = self.initial_cwnd
                    timeout_index += 1
                elif self.isCongestionAvoidance == 1:
                    self.current_cwnd += 1
                elif self.isThresh == 1:
                    self.current_cwnd *= 2
                    if self.current_cwnd >= self.ssthresh:
                        self.isThresh = 0
                        self.isCongestionAvoidance = 1
            i += 1
            self.yValues.append(self.current_cwnd)

    def plot_graph(self):
        fig = plt.figure(figsize=(9, 7), facecolor="#b5b0bf")
        ax = plt.axes()
        ax.set_facecolor("#b5b0bf")

        plt.xticks(self.xValues)
        right_side = ax.spines["right"]
        right_side.set_visible(False)
        top_line = ax.spines["top"]
        top_line.set_visible(False)

        fontsize = 15
        ax.plot(self.xValues, self.yValues, marker=".", color="#513f8f", linewidth=2, markerfacecolor="black", markersize=12)
        # plt.title("TCP Slow Start Simulation", fontdict={'fontsize': fontsize + 5})
        plt.xlabel("Packets sent (RTTs)", fontdict={'fontsize': fontsize})
        plt.ylabel("Size of cwnd (in MSS)", fontdict={'fontsize': fontsize})
        # plt.grid(True, color='#b5b0bf', linestyle='-', linewidth=2)
        # plt.gca().patch.set_facecolor('0.8')
        plt.show()

if __name__ == "__main__":
    # max_packets = int(input("Enter the number of packets to be sent: "))
    max_packets = 20
    # ssthresh = int(input("Enter the initial threshold: "))
    ssthresh = 8

    simulation = TCPSlowStartSimulation(max_packets, ssthresh)
    simulation.run_simulation()
    simulation.plot_graph()
