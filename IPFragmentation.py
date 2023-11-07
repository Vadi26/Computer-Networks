def ip_fragmentation_calculator(data_size, mtu):
    if data_size <= 0 or mtu <= 0:
        return "Data size and MTU must be greater than 0"

    fragments = data_size // mtu
    if data_size % mtu != 0:
        fragments += 1

    total_length = data_size if data_size <= mtu else mtu
    mf_flag = 0
    offset = 0

    fragmentation_info = {
        "Fragments": fragments,
        "Total Length": total_length,
        "MF Flag": mf_flag,
        "Offset": offset
    }

    return fragmentation_info

# Input values
data_size = int(input("Enter IP Data Packet size (in bytes): "))
mtu = int(input("Enter Maximum Transmission Unit (MTU) size (in bytes): "))

result = ip_fragmentation_calculator(data_size, mtu)
if isinstance(result, dict):
    print("IP Fragmentation Info:")
    for key, value in result.items():
        print(f"{key}: {value}")
else:
    print(result)
