"""Part 3 - Create/verify Loopback100 on IOS XE via RESTCONF.

"""
import os
import sys
import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HOST = os.getenv("IOSXE_HOST", "sandbox-iosxe-latest-1.cisco.com")
USER = os.getenv("IOSXE_USER", "developer")
PASS = os.getenv("IOSXE_PASS", "C1sco12345")

# CONFIG 
IF_NAME = "Loopback100"
IF_DESC = "Configured by ADHL automation"
IF_IP = "9.10.21.0"
IF_MASK = "255.255.255.255"
# ----------------------------------------------

URL = f"https://{HOST}/restconf/data/ietf-interfaces:interfaces/interface={IF_NAME}"
HEADERS = {"Accept": "application/yang-data+json", "Content-Type": "application/yang-data+json"}
AUTH = (USER, PASS)

payload = {
    "ietf-interfaces:interface": {
        "name": IF_NAME,
        "description": IF_DESC,
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {"address": [{"ip": IF_IP, "netmask": IF_MASK}]},
    }
}


def main():
    print("Payload:\n" + json.dumps(payload, indent=2))
    try:
        d = requests.delete(URL, headers={"Accept": HEADERS["Accept"]}, auth=AUTH, verify=False, timeout=15)
        print(f"DELETE (clean slate) status code: {d.status_code}")
        # PUT = create or replace the named interface (idempotent)
        r = requests.put(URL, headers=HEADERS, auth=AUTH, data=json.dumps(payload), verify=False, timeout=15)
    except requests.exceptions.RequestException as err:
        print(f"[ERROR] Connection failed: {err}")
        sys.exit(1)

    print(f"\nPUT status code: {r.status_code}")
    if r.status_code in (200, 201, 204):
        print(f"[SUCCESS] {IF_NAME} configured ({'created' if r.status_code == 201 else 'updated'}).")
    else:
        print(f"[FAILED] {r.status_code}: {r.text}")
        sys.exit(1)

    # Verify
    v = requests.get(URL, headers={"Accept": HEADERS["Accept"]}, auth=AUTH, verify=False, timeout=15)
    print(f"\nVerification GET status code: {v.status_code}")
    if v.status_code == 200:
        data = v.json()["ietf-interfaces:interface"]
        if isinstance(data, list):
            data = data[0]
        print(json.dumps(data, indent=2))
        addr = data.get("ietf-ip:ipv4", {}).get("address", [{}])[0]
        ok = data["name"] == IF_NAME and addr.get("ip") == IF_IP and data.get("enabled") is True
        print("\n[VERIFIED] Configuration matches." if ok else "\n[MISMATCH] Check configuration.")
    else:
        print(f"[ERROR] Could not verify: {v.text}")


if __name__ == "__main__":
    main()
