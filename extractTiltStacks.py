#!/usr/bin/python3
# ===================================================================
# Name:			extractTiltStacks
# Purpose:		Creates aligned tilt series stack from raw FISE movie.
# Called From:  User
# Author:       Fabian Eisenstein
# Revision:     v1.1
# Last Change:	2019/10/10: mean threshold factor to exclude frames, optimizations
#				2018/12/02
# Created:		2018/11/18
# ===================================================================

import sys
import os
import operator
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Creates aligned tilt series stack from raw FISE movie.')
parser.add_argument('inputStack',help='Path to raw FISE movie.')
parser.add_argument('outputStack',help='Base name for output stack.')
parser.add_argument('frameFile',help='Path to file containing saved frames (*_saved.txt).')
parser.add_argument('--meth',dest='meanthreshold',type=float,default=0,help='Mean count threshold factor. Exclude start/end frames of every tilt with a mean count less than neighbouring frames by this factor. Range: 0.0 - 1.0')
parser.add_argument('--b',dest='binfactor',default='1',help='Bin factor for frames before alignment. Default: 1')
parser.add_argument('--d',dest='frameDistance',type=int,default=5,help='Minimum number of missing frames to assume blanked beam. Default: 5')
parser.add_argument('--af_bin',dest='af_bin',default='2,1',help='Bin parameter for alignframes command. Requires 2 values. See IMOD alignframes man page. Default: 2,1')

args = parser.parse_args()
instack = args.inputStack
outstack = args.outputStack
savedFrames = args.frameFile

meanFactor = args.meanthreshold
binfactor = args.binfactor
frameDistance = args.frameDistance
af_bin = args.af_bin


def readSaved(raw):
	mics = []
	mic = []
	sec = 0
	lastLine = 0
	for line in raw:
		if int(line) == 0:
			sec = sec + 1		
			continue
		if int(line) <= int(lastLine) + frameDistance:
			mic.append(sec)
		else:
			if len(mic) > 0:
				mics.append(mic)
			mic = []
			mic.append(sec)	
		sec = sec + 1
		lastLine = line
	mics.append(mic)			#to add last tilt in case it ends without a jump in frames, if blank, additional tilt appears at end of stack
	return mics

if os.path.exists(savedFrames):
	if os.path.exists(instack): 

		savedFile = open(savedFrames,"r")
		micList = readSaved(savedFile)
		savedFile.close()

		if micList != []:
			newstackInputFile = str(len(micList)) + "\n"
			tiltno = 1
			for tilt in micList:
				if meanFactor > 0 and meanFactor < 1 and len(tilt) > 3:			#remove frames at start and end of tilt with mean count lower by input factor
					command = "newstack -bin " + binfactor + " -in " + instack + " -ou frameMeanTestStart.mrc -quiet -se " + str(tilt[0])
					os.system(command)
					meanStart = float(subprocess.check_output(["header","-mean","frameMeanTestStart.mrc"]).strip())

					command = "newstack -bin " + binfactor + " -in " + instack + " -ou frameMeanTestRef.mrc -quiet -se " + str(tilt[1])
					os.system(command)
					meanRef = float(subprocess.check_output(["header","-mean","frameMeanTestRef.mrc"]).strip())

					command = "newstack -bin " + binfactor + " -in " + instack + " -ou frameMeanTestEnd.mrc -quiet -se " + str(tilt[-1])
					os.system(command)
					meanEnd = float(subprocess.check_output(["header","-mean","frameMeanTestEnd.mrc"]).strip())

					if meanStart < meanFactor * meanRef:
						tilt.remove(tilt[0])
					if meanEnd < meanFactor * meanRef:
						tilt.remove(tilt[-1])

				command = "newstack -bin " + binfactor + " -in " + instack + " -ou " + outstack + "_" + str(tiltno).zfill(2) + ".mrc -quiet -se "
				for sec in tilt:
					command = command + str(sec) + ","
				command = command.strip(",")
				print(command)
				os.system(command)
				
				command = "alignframes -bin " + af_bin + " -in " + outstack + "_" + str(tiltno).zfill(2) + ".mrc -ou " + outstack + "_" + str(tiltno).zfill(2) + "_ali.mrc"
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
			print ("New output stack " + outstack + "_full.mrc was written!")
		else:
			print (savedFrames + " couldn't be read!\n")
	else:
		print (instack + " doesn't exist!\n")
else:
    print (savedFrames + " doesn't exist!\n")
