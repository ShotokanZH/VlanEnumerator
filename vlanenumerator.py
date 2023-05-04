#!/usr/bin/env python3
import argparse
import os
import threading
import time
from scapy.all import sniff, get_if_list, Dot1Q, packet

validvlans = []

def capture(pkt:packet):
    if pkt.haslayer(Dot1Q):
        vlanid = pkt[Dot1Q].vlan
        if not vlanid in validvlans:
            print("\tNew VLAN detected:", vlanid)
            validvlans.append(vlanid)

def main():
    ifaces = get_if_list()

    parser = argparse.ArgumentParser(description="VlanEnumerator v1.0 By ShotokanZH")
    parser.add_argument("interface", choices=ifaces, help="Network interface to use")
    parser.add_argument("--timeout", "-t", type=int, default=0, help="Listening time, 0 for unlimited (default)")
    args = parser.parse_args()

    euid = os.geteuid()
    if euid != 0:
        parser.error(f"You need to be root! (Expected EUID: 0, received: {euid})")

    print("Waiting for VLANs to appear..")
    try:
        if args.timeout:
            t = threading.Thread(target=sniff, kwargs={"iface": args.interface, "prn":capture})
            t.daemon = True
            t.start()
            print(f"Setting timeout: {args.timeout}s")
            time.sleep(args.timeout)
        else:
            sniff(iface=args.interface, prn=capture)
    except:
        print("")

    print("Detected vlans:")
    validvlans.sort()
    print(validvlans)


if __name__ == "__main__":
    main()
