#!/usr/bin/env python

rbllist = []

with open("rbllist.txt", "r") as rbltext:
    for line in rbltext:
        rbllist.append(line.strip())
rbltext.close()

ctr = 0

for rbl in rbllist:
    ctr += 1
    print (str(ctr) + " " + rbl)
