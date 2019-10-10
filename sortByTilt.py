#!/usr/bin/python3
# ===================================================================
# Name:			sortByTilt
# Purpose:		Reads .mdoc file or .tlt file, sorts stack by tilt angle and creates sorted stack and mdoc file
#				python sortByTilt.py [input stack] [output stack] [tilt file]
# Called From:  User, makeAlignedStack
# Author:       Fabian Eisenstein
# Revision:     v1.2 
# Last Change:	2019/10/10: create sorted dose file for IMOD, optimizations
#				2019/03/06: implemented reading of .tlt-like files
#				2018/03/13: minor text fixes
# Created:		2018/03/12
# ===================================================================

import sys
import os
import operator
import argparse

parser = argparse.ArgumentParser(description='Reads .mdoc file or .tlt file, sorts stack by tilt angle and creates sorted stack and .mdoc file.')
parser.add_argument('inputStack',help='Path to input stack.')
parser.add_argument('outputStack',help='Path to output stack.')
parser.add_argument('tiltFile',help='Path to .mdoc or .tlt file containing tilt angles.')
parser.add_argument('--dfile',dest='dfile',action='store_true',default=False,help='Create dose file for IMOD. Requires exposure dose set in .mdoc file or --dose input!')
parser.add_argument('--dose',dest='dose',type=float,default=0,help='Dose per tilt to write dose file for IMOD. Is ignored unless --dfile is set.')

args = parser.parse_args()
instack = args.inputStack
outstack = args.outputStack
mdocFileName = args.tiltFile

dfile = args.dfile
dose = args.dose

if dose > 0 and not dfile:
	print ("--dfile is not set. Dose value is ignored.")


def readMdoc(raw):                                                   		#Makes list of Mics for sorting
	raw.seek(0)
	mics = []
	mic = []
	totalDose = 0
	for line in raw:
		col = line.split(" ")
		if col[0] == "[ZValue":
			zval = col[2].split("]")
			mic.append(zval[0])
                	
		if col[0] == "TiltAngle":
			mic.append(float(col[2]))
			if dfile and dose > 0:
				mic.append(totalDose)
				mic.append(dose)
				totalDose += dose
			if not dfile or (dfile and dose > 0):
				mics.append(mic)
				mic = []
		if dfile and dose == 0 and col[0] == "ExposureDose":
			mic.append(totalDose)
			mic.append(float(col[2]))
			totalDose += float(col[2])
			mics.append(mic)
			mic = []

	return mics
	
def readTilt(raw):                                                   		#Makes list of Mics for sorting
	raw.seek(0)
	mics = []
	mic = []
	zval = 0
	totalDose = 0
	for line in raw:
		col = line.strip()
		mic.append(str(zval))
		mic.append(float(col))

		if dfile and dose > 0:
			mic.append(totalDose)
			mic.append(dose)
			totalDose += dose

		mics.append(mic)
		mic = []
		zval += 1
	return mics



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

	if os.path.exists(instack):

		command = "newstack -in " + instack + " -ou " + outstack + " -quiet "
		if mdoc == 1: 
			command = command + "-mdoc " 
		command = command + "-se "
		for mic in newmdocList:
			command = command + mic[0] + ","
		command = command.strip(",")

		print(command)
		if mdoc == 1 and instack.split('.')[0] != mdocFileName.split('.')[0]:
			os.system("cp " + mdocFileName + " " + instack + ".mdoc")

		os.system(command)
		if mdoc == 1 and instack != outstack and instack.split('.')[0] != mdocFileName.split('.')[0]:
			os.system("rm " + instack + ".mdoc")
		if mdoc ==1:
			print ("New mdoc file was written!")

		if dfile:
			doseoutput = ""
			for mic in newmdocList:
				if len(mic) > 3:
					doseoutput = doseoutput + str(mic[2]) + "\t" + str(mic[3]) + "\n"
				else:
					print ("Dose value was not found! No dose file written!")
					break
			if doseoutput != "":
				writeDose = open(outstack.split(".")[0] + "_dose.txt","w+")
				writeDose.seek(0,0)
				writeDose.write(doseoutput)
				writeDose.close()
				print ("Dose file was written!")

	else:
		print (instack + " doesn't exist!\n")
else:
	print (mdocFileName + " doesn't exist!\n")
