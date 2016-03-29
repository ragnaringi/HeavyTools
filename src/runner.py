#!/usr/bin/python

import shutil, errno, os, atexit, sys
from sys import argv

patchName = "Test"
outputDir = "heavy"

def clearTempFiles():
	shutil.rmtree(outputDir)

def processPatch(patchFolder):
	print("Compiling: " + patchFolder)

	if os.path.exists(outputDir):
		clearTempFiles()
	
	os.makedirs(outputDir)

	command = "python uploader.py " + patchFolder + " -n " + patchName + " -o " + outputDir
	os.system(command)
	os.system("cp bin/main.c heavy/main.c && cp bin/Makefile heavy/Makefile")
	os.system("cd heavy && make && ./main")

def exit_handler():
    print "Cleaning Up"
    clearTempFiles()

if len(argv) > 1:
	patchFolder = argv[1]
	processPatch(patchFolder)
else:
	print("Error: No folder provided")

atexit.register(exit_handler)