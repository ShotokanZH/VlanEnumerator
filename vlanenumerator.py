#!/usr/bin/env python3
import argparse
import re
import subprocess
import os
import threading
import time


def getInterfaces() -> list:
    with open("/proc/net/dev", "r") as nd:
        netdev = nd.read()
    interfaces = []
    for line in netdev.split("\n"):
        m = re.search(f"^\s*([a-z0-9]+):", line, re.MULTILINE)
        if m:
            iface = m.group(1)
            interfaces.append(iface)
    return interfaces


def capture(interface: str, validvlans: list):
    p = subprocess.Popen(("tcpdump", "-i", interface, "-nn", "-e", "vlan"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Waiting for VLANs to appear..")
    reg = re.compile(r",\s+length \d+: vlan (\d+),")
    for row in iter(p.stdout.readline, b''):
        m = re.search(reg, row.decode())
        if m:
            vlanid = int(m.group(1))
            if not vlanid in validvlans:
                print("\tNew VLAN detected:", vlanid)
                validvlans.append(vlanid)


def main():
    ifaces = getInterfaces()

    parser = argparse.ArgumentParser(description="VlanEnumerator v1.0 By ShotokanZH")
    parser.add_argument("interface", choices=ifaces, help="Network interface to use")
    parser.add_argument("--timeout", "-t", type=int, default=0, help="Listening time, 0 for unlimited (default)")
    args = parser.parse_args()

    euid = os.geteuid()
    if euid != 0:
        parser.error(f"You need to be root! (Expected EUID: 0, received: {euid})")

    validvlans = []

    try:
        if args.timeout:
            t = threading.Thread(target=capture, kwargs={"interface": args.interface, "validvlans": validvlans})
            t.daemon = True
            t.start()
            print(f"Setting timeout: {args.timeout}s")
            time.sleep(args.timeout)
        else:
            capture(args.interface, validvlans)
    except:
        print("")

    print("Detected vlans:")
    validvlans.sort()
    print(validvlans)


if __name__ == "__main__":
    main()
