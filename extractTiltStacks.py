#!/usr/bin/python3
# ===================================================================
# Name:		extractTiltStacks
# Purpose:	extract tilt series from FISE frame stack
# Called From:  User
# Author:       Fabian Eisenstein
# Revision:     v1.0 
# Last Change:	2019/08/05
# Created:	2018/11/18
# ===================================================================

import sys
import os
import operator

binfactor = "1"					# binning of frames before alignframes
alignframes_filter = "0.25"			# filter value for alignframes
alignframes_binning = "2,1"			# binning values for alignframes (bin for alignment, bin for summing)

#make input compatible with python 2.7
try:
   input = raw_input
except NameError:
   pass

def readSaved(raw):                          	#Makes list of frames to be summed
        mics = []
	mic = []
	sec = 0
	lastLine = 0
        for line in raw:
		if int(line) == 0:
			sec = sec + 1		
			continue
                if int(line) <= int(lastLine) + 5:
			mic.append(sec)
		else:
                        if len(mic) > 0:
				mics.append(mic)
			mic = []
                	mic.append(sec)	
		sec = sec + 1
		lastLine = line
	mics.append(mic)			#to add last tilt in case it ends without a jump in frames
        return mics

if len(sys.argv) == 4:
        instack = sys.argv[1]                   #if no arguments were given when script was called: ask for them
        outstack = sys.argv[2]
	savedFrames = sys.argv[3]
else:
        print ("Usage: python " + sys.argv[0] + " [input stack] [output base name] [saved frames file]")
        sys.exit("Missing arguments!")


if os.path.exists(savedFrames):               	#check if savedFrames file exists, then open it and read frames
        savedFile = open(savedFrames,"r")
        micList = readSaved(savedFile)
	savedFile.close()

	newstackInputFile = str(len(micList)) + "\n"
	tiltno = 1
	for tilt in micList:
		command = "newstack -bin " + binfactor + " -in " + instack + " -ou " + outstack + "_" + str(tiltno).zfill(2) + ".mrc -se "
		for sec in tilt:
			command = command + str(sec) + ","
		command = command.strip(",")
		print(command)
		os.system(command)
		
		command = "alignframes -vary " + alignframes_filter + " -bin " + alignframes_filter + " -shift 100 -in " + outstack + "_" + str(tiltno).zfill(2) + ".mrc -ou " + outstack + "_" + str(tiltno).zfill(2) + "_ali.mrc"
		print(command)
		os.system(command)

		newstackInputFile = newstackInputFile + outstack + "_" + str(tiltno).zfill(2) + "_ali.mrc\n0\n"

		tiltno = tiltno + 1

	newstackFile = open("aliframelist.txt","w+")
	newstackFile.seek(0,0)
        newstackFile.write(newstackInputFile)
	newstackFile.close()

	totalStackCommand = "newstack -filei aliframelist.txt -ou " + outstack + "_full.mrc"
	os.system(totalStackCommand)
		
else:
        print (savedFrames + " doesn't exist!\n")
