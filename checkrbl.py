#!/usr/bin/env python

# imports
import sys
import ipaddress
import dns.resolver
from timeit import default_timer as timer
import argparse

# Variable Declaration
rbllist = []
ctr = 0
IP = ""
dnsrecords = []

# Read RBL list into a list
def read_rbl_list():
    with open("rbllist.txt", "r") as rbltext:
        for line in rbltext:
            rbllist.append(line.strip())
    rbltext.close()

# Validate the IP address
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

# Check if the IP is a private or a public IP
def networkIP (ipaddr):
    if ipaddress.ip_address(ipaddr).is_private:
        print (ipaddr + " is a Private IP. Exiting..")
        sys.exit()
    else:
        return ipaddr

# Function to reverse an IP
def revIP (ipaddr):
    reverseIP = '.'.join((ipaddr).split(".")[::-1])
    return (reverseIP)

def rbl_lookup(ip):

    print ("\n\n" + ip + "\n\n")

    start = timer()
    errlist = []
    for rbl in rbllist:
        query_string = ip + "." + rbl
        
        print ("\nChecking" + query_string)

        dnsResolver = dns.resolver.Resolver()
        dnsResolver.timeout = 5
        dnsResolver.lifetime = 5
        try:
            dnsAnswer = dnsResolver.query(query_string, "A")
            if len(dnsAnswer) > 0:
                dnsrecords.append(ip)
                dnsrecords.append(rbl)
                txtAnswer = dnsResolver.query(query_string, "TXT")
                for rdata in txtAnswer:
                    dnsrecords.append(rdata)
        except Exception as e:
            errlist.append(rbl)
            errlist.append(e)
    end = timer()
    print(end - start) 
    print(dnsrecords)
    print (errlist)

def checkRBL (ipaddr):
    rev_ipaddr = revIP(ipaddr)
    read_rbl_list()

    rbl_lookup(rev_ipaddr)

def main():
    """
    Main function.
    Checks command-line arguments and calls the relevant function.
    """
    cli_argparser = argparse.ArgumentParser(description='')
    cli_argparser.add_argument('-i', '--ip', help="Enter the IP address to be checked", required=False)
    cli_argparser.add_argument('-d', '--domain', help="Enter the domain name to be checked", required=False)
    cli_args = cli_argparser.parse_args()

    if (cli_args.domain and cli_args.ip):
        print ("Invalid input. Enter either the IP address or the Domain name")
    elif (cli_args.ip):
        if validateIP(cli_args.ip):
            if networkIP(cli_args.ip):
                checkRBL(cli_args.ip)
    elif (cli_args.domain):
        print ("Domain")
        # Reverse look up domain and then test the IP
    else:
        print (cli_argparser.print_help())

if __name__ == '__main__':
    sys.exit(main())
