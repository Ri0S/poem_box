import sys
from heconvert.converter import e2h

if len(sys.argv) < 2:
	print('usage: python3 heconvert.py [word]')

print(e2h(sys.argv[1]))

