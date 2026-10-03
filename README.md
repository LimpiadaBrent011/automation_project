# Mini Network Automation Project

## Purpose
Reads a list of Cisco devices from `inventory.json`, checks whether each is UP or DOWN,
prints the result, and saves it to `output.json`.

## Files
- `inventory.json` - device list (hostname, ip, type, port, simulated_status)
- `network_check.py` - the checker
- `output.json` - generated results

## Usage
```bash
python network_check.py             # live: TCP connect to port 22 on each device
python network_check.py --simulate  # simulated: uses simulated_status from inventory.json
```

## Error handling
Missing/invalid inventory file, missing device fields, and unreachable devices
(timeout after 2 s -> DOWN) are all handled without crashing.
