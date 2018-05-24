#!/usr/bin/python

import shutil, errno, os, atexit, sys
from distutils.dir_util import copy_tree
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
	copy_tree(sys.path[0]+"/bin", outputDir)
	os.system("cd " + outputDir + " && make && ./main") # Compile and run

def exit_handler():
	print "Cleaning Up"
	clearTempFiles()

if len(argv) > 1:
	patchFolder = argv[1]
	processPatch(patchFolder)
else:
	print("Error: No folder provided")
	sys.exit()

atexit.register(exit_handler)