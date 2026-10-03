"""Mini network automation: read inventory.json, check each device, save output.json.

Real mode (default): TCP connect to the device's management port (SSH/22).
Simulate mode (--simulate): use "simulated_status" from inventory.json.
"""
import json
import socket
import sys
from datetime import datetime

INVENTORY = "inventory.json"
OUTPUT = "output.json"


def load_inventory(path):
    try:
        with open(path) as f:
            return json.load(f)["devices"]
    except FileNotFoundError:
        sys.exit(f"[ERROR] {path} not found.")
    except (json.JSONDecodeError, KeyError) as err:
        sys.exit(f"[ERROR] {path} is invalid: {err!r}")


def check_device(dev, simulate):
    if simulate:
        return dev.get("simulated_status", "DOWN").upper()
    try:
        with socket.create_connection((dev["ip"], dev.get("port", 22)), timeout=2):
            return "UP"
    except OSError:
        return "DOWN"


def main():
    simulate = "--simulate" in sys.argv
    results = []
    print(f"{'Hostname':<10} {'IP':<14} {'Type':<20} Status")
    print("-" * 52)
    for dev in load_inventory(INVENTORY):
        try:
            status = check_device(dev, simulate)
        except KeyError as err:
            print(f"[ERROR] Device entry missing field {err}: {dev}")
            continue
        print(f"{dev['hostname']:<10} {dev['ip']:<14} {dev['type']:<20} {status}")
        results.append({"hostname": dev["hostname"], "ip": dev["ip"], "status": status,
                        "checked_at": datetime.now().isoformat(timespec="seconds")})

    with open(OUTPUT, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved {len(results)} results to {OUTPUT} ({'simulated' if simulate else 'live'} mode)")


if __name__ == "__main__":
    main()

"""tungtungtungsahur#TripleT
