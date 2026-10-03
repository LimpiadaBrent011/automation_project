"""Part 1 - Network Inventory Tool (list of dictionaries)."""

devices = [
    {"hostname": "R1-HQ",    "mgmt_ip": "192.168.10.1", "device_type": "Cisco ISR 4331",     "location": "Head Office",   "status": "up"},
    {"hostname": "SW1-CORE", "mgmt_ip": "192.168.10.2", "device_type": "Cisco Catalyst 9300", "location": "Server Room",   "status": "up"},
    {"hostname": "SW2-ACC",  "mgmt_ip": "192.168.10.3", "device_type": "Cisco Catalyst 2960", "location": "Floor 2",       "status": "down"},
    {"hostname": "R2-BR",    "mgmt_ip": "192.168.20.1", "device_type": "Cisco CSR1000v",      "location": "Branch Office", "status": "up"},
]

HEADER = f"{'Hostname':<10} {'Mgmt IP':<15} {'Device Type':<22} {'Location':<15} {'Status':<6}"


def show(device_list, title):
    print(f"\n=== {title} ===")
    print(HEADER)
    print("-" * len(HEADER))
    for d in device_list:
        print(f"{d['hostname']:<10} {d['mgmt_ip']:<15} {d['device_type']:<22} {d['location']:<15} {d['status']:<6}")


def count_operational(device_list):
    return sum(1 for d in device_list if d["status"].lower() == "up")


if __name__ == "__main__":
    show(devices, "All Devices")
    up_devices = [d for d in devices if d["status"].lower() == "up"]
    show(up_devices, "Devices with status UP")
    print(f"\nOperational devices: {count_operational(devices)} of {len(devices)}")
