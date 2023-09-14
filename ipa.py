def checkvalidip(ip, c):
    p = ip.split('.')
    if len(p) != 4:
        return False
    
    fc = int(p[0])
    sc = int(p[1])
    if c == 'A':
        return fc == 10
    elif c == 'B':
        return (fc == 172 and sc >= 16 and sc <= 31)
    elif c == 'C':
        return (fc == 192 and sc == 168)
    return False


def checkvalidsubmask(m, c):
    if c == 'A':
        return 8 <= m <= 12
    elif c == 'B':
        return 16 <= m <= 24
    elif c == 'C':
        return 24 <= m <= 30
    return False

def bintodecimal(s):
    d = 0
    j = 0
    for i in range(len(s)-1,-1,-1):
        d += int(s[i]) * 2**j
        j+=1
    return d

def decimaltoip(d):
    b = bin(d)[2:]
    while len(b) != 32:
        b = '0' + b
    ansip = []
    for i in range(0,32,8):
        curr = b[i:i+8]
        a = bintodecimal(curr)
        ansip.append(a)
    return ansip

def iptodecimal(ip):
    j = 0
    d = 0
    for i in range(3,-1,-1):
        d += ip[i] * 256**j
        j+=1
    return d
        

def addipadress(ip1,ip2):
    d1 = iptodecimal(ip1)
    d2 = iptodecimal(ip2)
    s = d1 + d2
    ansip = decimaltoip(s)
    return ansip       
def printip(ip):
    return (f"{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}")
    
def andip(ip1,ip2):
    ansip = []
    for i in range(4):
        a = ip1[i] & ip2[i]
        ansip.append(a)
    return ansip

def setbitstoip(n):
    ansip = []
    while n >= 8:
        ansip.append(255)
        n-=8
    if n > 0:
        s = '1'*n
        s += '0'*(8-n)
        ansip.append(bintodecimal(s))
    while len(ansip) != 4:
        ansip.append(0)
    return ansip

def printallsubnets(c,ip,mask,sb):
    if c == 'A':
        ander = setbitstoip(8)
    elif c == "B":
        ander = setbitstoip(16)
    else:
        ander = setbitstoip(24)
        
    networkid = andip(ip,ander)
    curr = networkid
    if c == 'A':
        nb = 8
        hb = 24
    elif c == 'B':
        nb = 16
        hb = 16
    elif c == 'C':
        nb = 24
        hb = 8
    num_of_subnets = 2**(sb-nb)
    num_of_hosts_per_subnet = 2**(hb)//num_of_subnets - 2
    ip1 = decimaltoip(1)
    iphost = decimaltoip(num_of_hosts_per_subnet-1) 
    print(f"Number of subnets = {num_of_subnets}")
    print(f"Number of hosts per subnet = {num_of_hosts_per_subnet}")
    for i in range(1,num_of_subnets+1):
        print()
        print()
        print(f"Subnet {i}")
        print(f"Network Id: {printip(curr)}")
        curr = addipadress(curr,ip1)
        print(f"Start IP address: {printip(curr)}")
        curr = addipadress(curr,iphost)
        print(f"End IP address: {printip(curr)}")
        curr = addipadress(curr,ip1)
        print(f"Broadcast Id: {printip(curr)}")
        curr = addipadress(curr,ip1)
while True:        
    while True:
        c = input("Enter the class(A/B/C) : ")
        if c != 'A' and c != 'B' and c != 'C':
            print("Invalid Class!!! Please between A,B and C")
        else:
            break
        
    while True:
        if c == "A":
            print("The valid IP range for class A is 10.0.0.0 to 10.255.255.255")
        elif c == "B":
            print("The valid IP range for class B is 172.16.0.0 to 172.31.255.255")
        elif c == "C":
            print("The valid IP range for class C is 192.168.0.0 to 192.168.255.255")

        ip = input("Enter the IP address: ")
        if not checkvalidip(ip, c):
            print(f"Invalid IP address for Class {c}!")
        else:
            ip = [int(i) for i in ip.split('.')]
            break
        

        
    while True:
        if c == "A":
            print("For class A put values between /8 to /12(default /8)")
        elif c == "B":
            print("For class B put values between /16 to /24(default /16)")
        elif c == "C":
            print("For class C put values between /24 to /30(default /24)")
        mask = int(input("Enter the subnet mask in /x format: ").replace('/', ''))
        if not checkvalidsubmask(mask, c):
            print(f"Invalid mask for Class {c}!")
        else:
            break
            
    print(f"Subnet mask of the network is {printip(setbitstoip(mask))}")
    printallsubnets(c,ip,setbitstoip(mask),mask)
            
    choice = input("Do you wish to continue(y/n): ")
    if choice == "n" or choice == "N":
        break