#!/usr/bin/env python

# imports
import sys
import ipaddress
import dns.resolver
from timeit import default_timer as timer

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
    dnsrecords = []
    errlist = []
    rev_ipaddr = revIP(ipaddr)

    for rbl in rbllist:
        query_string = rev_ipaddr + "." + rbl
        
        dnsResolver = dns.resolver.Resolver()
        dnsResolver.timeout = 1
        dnsResolver.lifetime = 1
        try:
            dnsAnswer = dnsResolver.query(query_string, "A")
            if len(dnsAnswer) > 0:
                dnsrecords.append(ipaddr)
                dnsrecords.append(rbl)
                txtAnswer = dnsResolver.query(query_string, "TXT")
                for rdata in txtAnswer:
                    dnsrecords.append(rdata)
        except Exception as e:
            errlist.append(rbl)
            errlist.append(e)
    print (dnsrecords)
#    print (errlist)

if len(sys.argv) < 2:
    print ("Enter at least one IP")
elif len(sys.argv) > 2:
    print ("Enter only one IP")
else:
    IP = sys.argv[1]
    start = timer()
    if validateIP(IP):
        if networkIP(IP):
            checkRBL(IP)
    else:
        print ("Incorrect input, please try again. Exiting...")
    end = timer()
print(end - start)
