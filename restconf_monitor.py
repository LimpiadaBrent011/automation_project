"""Part 2 - RESTCONF monitor: GET /restconf/data/ietf-interfaces:interfaces"""
import os
import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # sandbox uses self-signed cert

# Cisco DevNet Always-On IOS XE sandbox (override with env vars if your reservation differs)
HOST = os.getenv("IOSXE_HOST", "sandbox-iosxe-latest-1.cisco.com")
USER = os.getenv("IOSXE_USER", "developer")
PASS = os.getenv("IOSXE_PASS", "C1sco12345")

URL = f"https://{HOST}/restconf/data/ietf-interfaces:interfaces"
HEADERS = {"Accept": "application/yang-data+json"}


def main():
    try:
        resp = requests.get(URL, headers=HEADERS, auth=(USER, PASS), verify=False, timeout=10)
    except requests.exceptions.RequestException as err:
        print(f"[ERROR] Could not connect to {HOST}: {err}")
        sys.exit(1)

    print(f"HTTP Status Code: {resp.status_code}")
    if resp.status_code != 200:
        print(f"[ERROR] Request failed: {resp.text}")
        sys.exit(1)

    interfaces = resp.json()["ietf-interfaces:interfaces"]["interface"]
    print(f"\n{'Interface':<25} {'Enabled':<8}")
    print("-" * 34)
    for intf in interfaces:
        print(f"{intf['name']:<25} {str(intf.get('enabled')):<8}")


if __name__ == "__main__":
    main()
