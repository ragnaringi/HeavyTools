#!/usr/bin/python

import shutil, errno, os, atexit
from sys import argv

patchName = "Test"
outputDir = "temp"

def clearTempFiles():
	shutil.rmtree(outputDir)

def processPatch(patchFolder):
	print("Compiling: " + patchFolder)

	if os.path.exists(outputDir):
		clearTempFiles()
	
	os.makedirs(outputDir)

	os.system("hv-uploader " + patchFolder + " -n " + patchName + " -o " + outputDir + " -g c-src") # Upload
	os.system("cp bin/main.c " + outputDir+"/main.c && cp bin/Makefile " + outputDir+"/Makefile") # Prepare files
	os.system("cd " + outputDir + " && make && ./main") # Compile and run

def exit_handler():
	print "Cleaning Up"
	clearTempFiles()

if len(argv) > 1:
	patchFolder = argv[1]
	processPatch(patchFolder)
else:
	print("Error: No folder provided")

atexit.register(exit_handler)