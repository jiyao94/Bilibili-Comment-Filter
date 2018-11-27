#!/usr/bin/python3

import binascii
#import xml.etree.ElementTree as ET
#from sys import stdout

with open('crc32_1-10000000.txt', 'w') as f:
	for i in range(10000000):
		f.write(hex(binascii.crc32(bytes(str(i+1), 'utf-8')))[2:] + '\n')
'''
for filename in os.listdir():
	if len(filename) > 4 and filename[-4:] == '.xml':
		os.system('cp {0} {0}.bak'.format(filename))
		break
if filename[-4:] != '.xml':
	raise Exception('xml file not exsit.')

tree = ET.parse(filename)
root = tree.getroot()

with open('crc32_1-10000000.txt') as f:
	uid_h_lst = f.readlines()

for comment in root.findall('d'):
	info, text = comment.get('p').split(','), comment.text
	uid_h = info[6]
	if uid_h not in uid_h_lst:
		#print(info, text)
		stdout.write('.')
		stdout.flush()
		root.remove(comment)
print()
tree.write(filename, 'utf-8')
'''