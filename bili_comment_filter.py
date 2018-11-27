#!/usr/bin/python3

import Levenshtein, os
import xml.etree.ElementTree as ET
from collections import namedtuple

def Preprocess(text):
	text = list(text.lower())
	junklst = '`~!@#$%^&*()_+-={\\}[]|;\':",./<>? '
	junklst += '·～！￥……（）——【】、；’：“”，。《》？'
	for i in junklst:
		while i in text:
			text.remove(i)
	for i in range(len(text)-1, 2, -1):
		if text[i-3] == text[i-2] == text[i-1] == text[i]:
			del text[i]
	for i in range(len(text)-1, 4, -2):
		if text[i-4] == text[i-2] == text[i] and text[i-5] == text[i-3] == text[i-1]:
			del text[i], text[i-1]
	text = ''.join(text)
	return text

for filename in os.listdir():
	if len(filename) > 4 and filename[-4:] == '.xml':
		os.system('cp {0} {0}.bak'.format(filename))
		break
if filename[-4:] != '.xml':
	raise Exception('xml file not exsit.')

CommentTuple = namedtuple('CommentTuple', 'time, text, comment')
similarity = 0.5
comments = {}

tree = ET.parse(filename)
root = tree.getroot()
for comment in root.findall('d'):
	time = float(comment.get('p').split(',')[0])
	commenttuple = CommentTuple(time, Preprocess(comment.text), comment)
	timeslot = int(time//30)
	if timeslot not in comments:
		comments[timeslot] = {commenttuple: [commenttuple]}
	else:
		comments[timeslot][commenttuple] = [commenttuple]

for i in range(max(comments) + 1):
	if i not in comments:
		continue
	groups = []
	for k in comments[i].copy():
		group = comments[i].pop(k)
		if i-1 in comments:
			for kk in comments[i-1].copy():
				for c in comments[i-1][kk]:
					if Levenshtein.ratio(k.text, c.text) >= similarity:
						group += comments[i-1].pop(kk)
						break
		for g in groups[:]:
			for c in g:
				if Levenshtein.ratio(k.text, c.text) >= similarity:
					group += g
					groups.remove(g)
					break
		groups.append(group)
	for g in groups:
		texts = [i.text for i in g]
		key = g[texts.index(Levenshtein.setmedian(texts))]
		comments[int(key.time//30)][key] = g

myroot = ET.Element(root.tag)
mytree = ET.ElementTree(myroot)
for i in range(7):
	ET.SubElement(myroot, root[i].tag).text = root[i].text
for t in comments:
	for c in comments[t]:
		length = len(comments[t][c])
		if length > 1:
			c.comment.text += '[x{0}]'.format(length)
			print(c.time, c.comment.text, [i.text for i in comments[t][c]])
		myroot.append(c.comment)
mytree.write(filename, 'utf-8', True)