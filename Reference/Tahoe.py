import matplotlib.pyplot as plt


number_of_packets = int(input("Enter the number of packets to be sent: "))
ssthresh = int(input("Enter the initial threshold: "))
timeout_list = [int(x) for x in input("Enter at what packets the timeout/ 3 ACKs arrive with spaces in between: ").split()]
x_coordinates = []
y_coordinates = []
initial_cwnd = 1
ss_flag = 1
ca_flag = 0
current_cwnd = 1
fig = plt.figure(figsize=(9, 7), facecolor="#b5b0bf")
ax = plt.axes()
ax.set_facecolor("#b5b0bf")
i=1
while i <=(number_of_packets):
    x_coordinates.append(i)
    if(i == 1):
        current_cwnd = initial_cwnd
    else:
        if i-1 in timeout_list:
            ss_flag = 1
            if ca_flag:
                ca_flag = 0
            print((i,current_cwnd))
            ssthresh = int(current_cwnd/2)
            current_cwnd = initial_cwnd
        elif current_cwnd >= ssthresh and ca_flag == 0:         
            current_cwnd = ssthresh
            ca_flag = 1
            ss_flag = 0
            current_cwnd = current_cwnd + 1
        elif ca_flag == 1:
            current_cwnd = current_cwnd + 1
        elif ss_flag == 1:
            current_cwnd = current_cwnd*2
            if current_cwnd > ssthresh:
                current_cwnd = ssthresh
    i+=1
    y_coordinates.append(current_cwnd)

plt.xticks(x_coordinates)
right_side = ax.spines["right"]
right_side.set_visible(False)
top_line = ax.spines["top"]
top_line.set_visible(False)
fontsize = 15
ax.plot(x_coordinates, y_coordinates, marker = ".", color = "#513f8f", linewidth=2,markerfacecolor='black', markersize=12)
plt.title("TCP Taho", fontdict={'fontsize': fontsize + 5}) 
plt.xlabel("Packets sent (RTTs)", fontdict={'fontsize': fontsize}) 
plt.ylabel("Size of cwnd  (in MSS)", fontdict={'fontsize': fontsize})
plt.grid(True, color='#b5b0bf', linestyle='-', linewidth=2)
plt.gca().patch.set_facecolor('0.8')
plt.show()

