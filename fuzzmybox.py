#!/bin/python

import sys, getopt, os
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

import random
from array import *

try:
    from scapy.all import * #Required for Scapy 2.0 and above
except:
    from scapy import * #Scapy 1.0

from scapy.utils import rdpcap
from scapy.layers.inet import IP,UDP,TCP
from scapy.packet import Raw

def main(argv):
	inputfile = ''
	outputfile = ''
	hookfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:t:",["ifile=","ofile=","transformation="])
	except getopt.GetoptError:
		print sys.argv[0] + ' -i inputfile -o outputfile -t [hook script]'
		print sys.argv[0] + ' -i sample.pcap -o result.pcap -t example'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		elif opt in ("-t", "--transformation"):
			hookfile = arg

	pkts=rdpcap(inputfile)
	for pkt in pkts:
	    try:
		my_array = []
		if pkt.haslayer(TCP):
		    for d in str(pkt.getlayer(TCP).payload):
		        my_array.append(d)
		if pkt.haslayer(UDP):
		    for d in str(pkt.getlayer(UDP).payload):
		        my_array.append(d)
		
		modname = "hooks." + hookfile
		module = __import__(modname, globals(), locals(), ['modify_payload'])
		func = getattr(module, "modify_payload")
		data = func(my_array)
		str1 = ''.join(data)
		
		#replace payload in origional packet
		if pkt.haslayer(TCP):
		    pkt.getlayer(TCP).payload=str1
		if pkt.haslayer(UDP):
		    pkt.getlayer(UDP).payload=str1
		    
	    except:
		raise
	wrpcap(outputfile, pkts)

total = len(sys.argv)
main(sys.argv[1:])
