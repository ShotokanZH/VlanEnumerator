# 🌐 VlanEnumerator by ShotokanZH

This Python script 🐍 enumerates **tagged** VLANs 🏷️ present on a specific network interface. 

## Prerequisites
- Python >= 3.7 🐍
- scapy >= 2.5.0

To rapidly install all the dependencies (scapy) just run:
```
python3 -m pip install requirements.txt
```

## Usage
```
usage: vlanenumerator.py [-h] [--timeout TIMEOUT] {<interface>}

VlanEnumerator v1.0 By ShotokanZH

positional arguments:
  {<interface>}             Network interface to use

options:
  -h, --help            show this help message and exit
  --timeout TIMEOUT, -t TIMEOUT
                        Listening time, 0 for unlimited (default)
```
Replace `<interface>` with the name of the network interface you want to enumerate VLANs on.

Note: this script needs to be run by root (euid == 0)

## Output
The script will output a list of VLAN IDs that are currently tagged on the specified network interface.

```
~# python3 -BO vlanenumerator.py eth0 -t 10
Setting timeout: 10s
Waiting for VLANs to appear..
    New VLAN detected: 10
    New VLAN detected: 50
    New VLAN detected: 1043
    New VLAN detected: 40
    New VLAN detected: 27
Detected vlans:
[10,27,40,50,1043]
```
