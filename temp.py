def listToIP(ipList):
    ans = ""
    for i in range(len(ipList)):
        ans += str(ipList[i])
        ans += '.'
    ans = ans[:-1]
    return ans

print(listToIP([255,43,21,33]))




def printAllSubnets(classType, IP, numOfSubnets, numOfHosts, networkID, setBits):
    nwNum = list(map(int, networkID.split('.')))
    startAddress = list(map(int, networkID.split('.')))
    endAddress = list(map(int, networkID.split('.')))
    bcNum = endAddress.copy()
    intialInc = 1 << ((8 - setBits)%8)
    inc = 0
    number = 0
    if (classType == 'A'):
        number = 2**(16 - setBits)
        endAddress[2] = 255
        endAddress[3] = 254
        for i in range(1, numOfSubnets + 1):
            print(f"Subnet {i} -> ")
            startAddress = nwNum.copy()
            print("Network ID : ", listToIP(nwNum))
            startAddress[3] += 1
            print("Start Address : ", listToIP(startAddress))
            endAddress[1] = (64*i) - 1
            print("End Address : ", listToIP(endAddress))
            bcNum = endAddress.copy()
            bcNum[3] += 1
            print("Broadcast Address : ", listToIP(bcNum))
            print()
            nwNum[1] = 64*i

    elif (classType == 'B'):
        endAddress[3] = 254
        for i in range(1, numOfSubnets + 1):
            print(f"Subnet {i} -> ")
            startAddress = nwNum.copy()
            print("Network ID : ", listToIP(nwNum))
            startAddress[len(startAddress) - 1] += 1
            print("Start Address : ", listToIP(startAddress))
            endAddress[2] = (16*i) - 1
            print("End Address : ", listToIP(endAddress))
            bcNum = endAddress.copy()
            bcNum[3] += 1
            print("Broadcast Address : ", listToIP(bcNum))
            print()

    elif (classType == 'C'):
        for i in range(1, numOfSubnets + 1):
            print(f"Subnet {i} -> ")
            print("Network ID : ", listToIP(nwNum))
            startAddress[len(startAddress) - 1] += 1
            print("Start Address : ", listToIP(startAddress))
            endAddress[1] = (64*i) - 1
            print("End Address : ", listToIP(endAddress))
            bcNum = endAddress.copy()
            bcNum[3] += 1
            print("Broadcast Address : ", listToIP(bcNum))
            print()
