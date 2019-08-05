#!/usr/bin/python3
# ===================================================================
# Name:		sortByTilt
# Purpose:	Reads mdoc file, sorts stack by tilt angle and creats sorted stack and mdoc file
#		python sortByTilt.py [input stack] [output stack] [mdoc file]
# Called From:  User, makeAlignedStack
# Author:       Fabian Eisenstein
# Revision:     v1.1 
# Last Change:	2019/03/06: implemented reading of .tlt-like files
#		2018/03/13: minor text fixes
# Created:	2018/03/12
# ===================================================================

import sys
import os
import operator

#make input compatible with python 2.7
try:
	input = raw_input
except NameError:
	pass

def readMdoc(raw):                                                   		#Makes list of Mics for sorting
	raw.seek(0)
	mics = []
	mic = []
	for line in raw:
		col = line.split(" ")
		if col[0] == "[ZValue":
			zval = col[2].split("]")
			mic.append(zval[0])
                	
		if col[0] == "TiltAngle":
			mic.append(float(col[2]))
			mics.append(mic)
			mic = []	
	return mics
	
def readTilt(raw):                                                   		#Makes list of Mics for sorting
	raw.seek(0)
	mics = []
	mic = []
	zval = 0
	for line in raw:
		col = line.strip()
		mic.append(str(zval))
		mic.append(float(col))
		mics.append(mic)
		mic = []
		zval += 1
	return mics

if len(sys.argv) == 4:
	instack = sys.argv[1]                                              	#if no arguments were given when script was called: ask for them
	outstack = sys.argv[2]
	mdocFileName = sys.argv[3]
else:
	print ("Usage: python " + sys.argv[0] + " [input stack] [output stack] [mdoc/tlt file]")
	sys.exit("Missing arguments!")


if os.path.exists(mdocFileName):                                                #check if mdoc file exist, then open it and read tilts
	mdocFile = open(mdocFileName,"r")
	mdocList = readMdoc(mdocFile)
	
	if mdocList == []:
		mdocList = readTilt(mdocFile)
		if mdocList == []:
			sys.exit("Mdoc or tilt file could not be read!")
		else:
			mdoc = 0
	else:
		mdoc = 1
	mdocFile.close()

	newmdocList = sorted(mdocList, key=operator.itemgetter(1))		#sorts list of mics by tilt

	command = "newstack -in " + instack + " -ou " + outstack + " "
	if mdoc == 1: 
		command = command + "-mdoc " 
	command = command + "-se "
	for mic in newmdocList:
		command = command + mic[0] + ","
	command = command.strip(",")

	print(command)
	os.system("cp " + mdocFileName + " " + instack + ".mdoc")
	os.system(command)
	if instack != outstack:
		os.system("rm " + instack + ".mdoc") 

else:
	print (mdocFileName + " doesn't exist!\n")
