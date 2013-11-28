#!/bin/python

import sys, getopt
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

def shuffle(x):
    x = list(x)
    random.shuffle(x)
    return x

def main(argv):
	inputfile = ''
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print 'test.py -i <inputfile> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
	#print 'Input file is: ', inputfile
	#print 'Output file is: ', outputfile

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
		
		#fuzzing framework goes here
		data = shuffle(my_array)
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
if len (sys.argv) != 5 :
	print sys.argv[0] + ' -i <inputfile> -o <outputfile>'
	sys.exit(2)
main(sys.argv[1:])
