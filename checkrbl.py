#!/usr/bin/env python

# imports
import sys
import ipaddress

rbllist = []
ctr = 0
IP = ""

with open("rbllist.txt", "r") as rbltext:
    for line in rbltext:
        rbllist.append(line.strip())
rbltext.close()

def validateIP(ipaddr):
    try:
        ipaddress.ip_address(ipaddr)
        if ipaddress.IPv4Address(ipaddr):
           return 1
        elif ipaddress.IPv6Address(ipaddr):
            return 1
        else:
            return 0
    except ValueError as e:
        print (e.args[0])

def networkIP (ipaddr):
    if ipaddress.ip_address(ipaddr).is_private:
        print (ipaddr + " is a Private IP. Exiting..")
        sys.exit()
    else:
        return ipaddr

def revIP (ipaddr):
    reverseIP = '.'.join((ipaddr).split(".")[::-1])
    return (reverseIP)

def checkRBL (ipaddr):
    rev_ipaddr = revIP(ipaddr)
    query_string = rev_ipaddr + "." + rbllist[0]
    print (query_string)

if len(sys.argv) < 2:
    print ("Enter at least one IP")
elif len(sys.argv) > 2:
    print ("Enter only one IP")
else:
    #print (sys.argv[1])
    IP = sys.argv[1]
    if validateIP(IP):
        if networkIP(IP):
            checkRBL(IP)
    else:
        print ("Incorrect input, please try again. Exiting...")
