from tabulate import tabulate

def helper(num_set_bits):
    result = 255
    num = 0
    for _ in range(8 - num_set_bits):
        num = (num << 1) | 1

    result = result ^ num

    return result

def number_with_set_bits(num_set_bits):
    ans = []
    while(num_set_bits > 7):
        ans.append(255)
        num_set_bits -= 8
    
    if (num_set_bits > 0):
        ans.append(helper(num_set_bits))

    while (len(ans) != 4):
        ans.append(0)

    return ans

def listToIP(ipList):
    ans = ""
    for i in range(len(ipList)):
        ans += str(ipList[i])
        ans += '.'
    ans = ans[:-1]
    return ans

def broadcastID(numbers):
    bcID = ""
    complement = []
    for i in range(len(numbers)):
        complement.append(numbers[i] ^ 255)

    for i in range(len(numbers)):
        result = complement[i] | ipNumbers[i]
        bcID += (str(result))
        bcID += "."

    bcID = bcID[:-1]
    return bcID

def printAllSubnets(classType, IP, numOfSubnets, numOfHosts, networkID, setBits):
    nwNum = list(map(int, networkID.split('.')))
    startAddress = list(map(int, networkID.split('.')))
    endAddress = list(map(int, networkID.split('.')))
    bcNum = endAddress.copy()
    intialInc = 1 << (8 - setBits)%8
    inc = intialInc
    output = []
    temp = []
    if (classType == 'A'):
        endAddress[2] = 255
        endAddress[3] = 254 
        for i in range(1, numOfSubnets + 1):
            # print(f"Subnet {i} -> ")
            startAddress = nwNum.copy()
            # print("Network ID : ", listToIP(nwNum))
            startAddress[3] += 1
            # print("Start Address : ", listToIP(startAddress))
            endAddress[1] = inc - 1
            # print("End Address : ", listToIP(endAddress))
            bcNum = endAddress.copy()
            bcNum[3] += 1
            # print("Broadcast Address : ", listToIP(bcNum))
            print()
            output.append([listToIP(nwNum), listToIP(startAddress), listToIP(endAddress), listToIP(bcNum)])
            nwNum[1] = inc
            inc += intialInc

    elif (classType == 'B'):
        endAddress[3] = 254
        for i in range(1, numOfSubnets + 1):
            # print(f"Subnet {i} -> ")
            startAddress = nwNum.copy()
            # print("Network ID : ", listToIP(nwNum))
            startAddress[3] += 1
            # print("Start Address : ", listToIP(startAddress))
            endAddress[2] = inc - 1
            # print("End Address : ", listToIP(endAddress))
            bcNum = endAddress.copy()
            bcNum[3] += 1
            # print("Broadcast Address : ", listToIP(bcNum))
            print()
            output.append([listToIP(nwNum), listToIP(startAddress), listToIP(endAddress), listToIP(bcNum)])
            nwNum[2] += inc
            inc += intialInc

    elif (classType == 'C'):
        for i in range(1, numOfSubnets + 1):
            # print(f"Subnet {i} -> ")
            startAddress = nwNum.copy()
            # print("Network ID : ", listToIP(nwNum))
            startAddress[3] += 1
            # print("Start Address : ", listToIP(startAddress))
            endAddress[3] = inc - 2
            # print("End Address : ", listToIP(endAddress))
            bcNum = endAddress.copy()
            bcNum[3] += 1
            # print("Broadcast Address : ", listToIP(bcNum))
            print()
            output.append([listToIP(nwNum), listToIP(startAddress), listToIP(endAddress), listToIP(bcNum)])
            nwNum[3] = inc
            inc += intialInc

    print(tabulate(output, headers=["Network Address", "Start Address", "End Address", "Broadcast Address"], tablefmt="fancy_grid"))

while (True):    
    classType = str(input("Enter the class : "))
    subnetMask = ""
    rangeOfIP = ""
    if (classType == 'A'):
        subnetMask = "255.0.0.0"
        rangeOfIP = "10.0.0.0 to 10.255.255.255"
        classTypenum = 8
        break
    elif (classType == 'B'):
        subnetMask = "255.255.0.0"
        rangeOfIP = "172.16.0.0 to 172.31.255.255"
        classTypenum = 16
        break
    elif (classType == 'C'):
        subnetMask = "255.255.255.0"
        rangeOfIP = "192.168.0.0 to 192.168.255.255"
        classTypenum = 24
        break
    else:
        print("Invalid input ! Try again")

while True:
    choice = str(input("Do you want the default subnet mask (/8 for A, /16 for B, /24 for C)?"))
    if (choice == 'n'):
        classTypenum = str(input("Enter no.of set bits : "))
        classTypenum = classTypenum[1::]
        classTypenum = int(classTypenum)
        subnetMasklist = number_with_set_bits(classTypenum)
        subnetMask = ""
        for i in subnetMasklist:
            subnetMask += str(i)
            subnetMask += '.'
        subnetMask = subnetMask[:-1]
        break
    elif (choice == 'y'):
        break
    else:
        print("Invalid input! Try again")

print("Subnet Mask for your selected class is -> ", subnetMask)

if (classType == 'A'):
    print("The valid IP range for class A is ", rangeOfIP)
elif (classType == 'B'):
    print("The valid IP range for class B is ", rangeOfIP)
else:
    print("The valid IP range for class C is ", rangeOfIP)

while True:
    IP = str(input("Enter valid IP address : "))
    nums = IP.split('.')
    if (len(nums) != 4):
        print("Invalid IP ! Please try again !")
        continue
    if (classType == 'A'):
        if (nums[0] == '10'):
            break
        else:
            print("Invalid IP ! Please try again !")
    elif (classType == 'B'):
        if (nums[0] == '172' and nums[1] >= '16' and nums[1] <= '31'):
            break
        else:
            print("Invalid IP ! Please try again !")
    elif (classType == 'C'):
        if (nums[0] == '192' and nums[1] == '168'):
            break
        else:
            print("Invalid IP ! Please try again !")
    else:
        break

numbers = list(map(int, subnetMask.split('.')))

ipNumbers = list(map(int, IP.split('.')))

nwID = ""
for i in range(len(numbers)):
    result = numbers[i] & ipNumbers[i]
    nwID += (str(result))
    nwID += "."

nwID = nwID[:-1]

print("Network ID : ", nwID)

bcID = ""
complement = []
for i in range(len(numbers)):
    complement.append(numbers[i] ^ 255)

for i in range(len(numbers)):
    result = complement[i] | ipNumbers[i]
    bcID += (str(result))
    bcID += "."

bcID = bcID[:-1]

print("Broad cast ID : ", bcID)

num_of_subnets = 0
if (classType == 'A'):
    num_of_subnets = 2**(classTypenum - 8)
    print("No.of subnets -> ", 2**(classTypenum - 8))
elif (classType == 'B'):
    num_of_subnets = 2**(classTypenum - 16)
    print("No.of subnets -> ", 2**(classTypenum - 16))
else:
    num_of_subnets = 2**(classTypenum - 24)
    print("No.of subnets -> ", 2**(classTypenum - 24))

num_of_hosts = 2**(32 - classTypenum) - 2
if (classType == 'A'):
    print("No.of hosts per subnet -> ", 2**(32 - classTypenum) - 2)
elif (classType == 'B'):
    print("No.of hosts per subnet -> ", 2**(32 - classTypenum) - 2)
else:
    print("No.of hosts per subnet -> ", 2**(32 - classTypenum) - 2)

# printAllSubnets(IP, subnetMask, num_of_subnets)  # Change the second argument based on the desired number of subnets
printAllSubnets(classType, IP, num_of_subnets, num_of_hosts, nwID, classTypenum)