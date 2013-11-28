import random

def modify_payload(data):
	x = list(data)
	random.shuffle(x)
	return x

