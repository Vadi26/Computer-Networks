import matplotlib.pyplot as plt


number_of_packets = int(input("Enter the number of packets to be sent: "))
ssthresh = int(input("Enter the initial threshold: "))
timeout_list = [int(x) for x in input("Enter at what packets the timeout occurs with spaces in between: ").split()]
dupACK_list =  [int(x) for x in input("Enter at what packets duplicate ACKs arrive with spaces in between: ").split()]
threedupACK_list =  [int(x) for x in input("Enter at what packets 3 duplicate ACKs arrive with spaces in between: ").split()]

x_coordinates = []
y_coordinates = []

fig = plt.figure(figsize=(9, 7), facecolor="#b5b0bf")
ax = plt.axes()
ax.set_facecolor("#b5b0bf")
ss_flag = 1
ca_flag = 0
fr_flag = 0
initial_cwnd = 1
current_cwnd = 1
temp_cwnd = 1
dupACKcount=0
for i in range(1,number_of_packets+1):
    if(i == 1):
        current_cwnd = initial_cwnd
    else:
        if i in timeout_list:
            if ca_flag==1:
                ca_flag=0
            if fr_flag==1:
                fr_flag=0
            ss_flag=1
            ssthresh=int(current_cwnd/2)
            current_cwnd=initial_cwnd
        elif i-1 in dupACK_list:
            if ss_flag==1:
                ss_flag=0
                dupACKcount+=1
                current_cwnd*=2
            elif ca_flag==1:
                ca_flag=0
                dupACKcount+=1
            else:
                current_cwnd=current_cwnd+1    

        elif i-1 in threedupACK_list:
            if ss_flag==1:
                ss_flag=0
            elif ca_flag==1:
                ca_flag=0
            fr_flag=1
            ssthresh=int(current_cwnd/2)
            current_cwnd=ssthresh+3
        else:
            if ss_flag==1:
                current_cwnd*=2
            elif ca_flag==1:
                current_cwnd+=1
            else:
                current_cwnd=ssthresh
                fr_flag=0   
                ca_flag=1
            dupACKcount=0
            if current_cwnd>=ssthresh:
                ss_flag=0
                ca_flag=1
    x_coordinates.append(i)
    y_coordinates.append(current_cwnd)
    


plt.xticks(x_coordinates)

right_side = ax.spines["right"]
right_side.set_visible(False)

top_line = ax.spines["top"]
top_line.set_visible(False)

fontsize = 15
ax.plot(x_coordinates, y_coordinates, marker = ".", color = "#513f8f", linewidth=2,markerfacecolor='black', markersize=12)
plt.title("TCP Reno", fontdict={'fontsize': fontsize + 5}) 
plt.xlabel("Packets sent (RTTs)", fontdict={'fontsize': fontsize}) 
plt.ylabel("Size of cwnd  (in MSS)", fontdict={'fontsize': fontsize})


plt.grid(True, color='#b5b0bf', linestyle='-', linewidth=2)
plt.gca().patch.set_facecolor('0.8')




plt.show()