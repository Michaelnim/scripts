#!/usr/bin/env python3

import os
import sys
import shutil
import socket

def check_reboot():
    ##Testing for github 
    ##Returns True if the computer has a pending reboot.
    return os.path.exists("/run/reboot - required")

def check_disk_full(disk, min_gb, min_percent):
    #Returns true if there isnt enough disk space, false otherwise
    du = shutil.disk_usage(disk)
    #Calculate the percent of free space
    percent_free = 100 * du.free / du.total
    gigabytes_free = du.free / 2**30
    if percent_free < min_percent or gigabytes_free < min_gb:
        return True
    return False

def check_root_full():
    #Returns true if root partition is full, False otherwise
    return check_disk_full(disk="/", min_gb=2, min_percent=10)

def check_no_network():
    #Returns true if it fails to resolve google's url, False otherwise
    try:
        socket.gethostbyname("www.google.com")
        return False
    except:
        return True

def main():
    checks = [
        (check_reboot, "Pending Reboot"),
        (check_root_full, "Root partition is full"),
        (check_no_network, "No working network"),
    ]
    everything_ok = True
    for check, msg in checks:
        if check():
            print(msg)
            everything_ok = False

    if not everything_ok:
        sys.exit(1)

    print("Everything ok.")
    sys.exit(0)

main()