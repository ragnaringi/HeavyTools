#!/usr/bin/python

import shutil, errno, os, atexit, sys
from distutils.dir_util import copy_tree
from sys import argv
from glob import glob
from os.path import join

def clearTempFiles():
	if os.path.exists("temp"):
		shutil.rmtree("temp")

def getLibraryName(srcDir):
	file = [filename for filename in os.listdir(srcDir) if filename.startswith("Heavy_")][0]
	return (os.path.splitext(file)[0])

def getFilesWithExtension(srcDir, extensions):
	files = []
	for ext in extensions:
		files.extend(glob(join(srcDir, ext)))
	return files

def copyHeaders(srcDir, dstDir):
	print("Copy headers")
	for file in getFilesWithExtension(srcDir,('*.h', '*.hpp')):
		if os.path.isfile(file):
			shutil.copy2(file, dstDir)

def copyLibrary(srcDir, dstDir):
	print("Copy library")
	for file in getFilesWithExtension(srcDir,('*.a', '*.so')):
		if os.path.isfile(file):
			shutil.copy2(file, dstDir)

def compileSource(srcDir, targetName, dstDir):
	print("Compiling: " + srcDir)

	clearTempFiles()
	

	if os.path.exists(dstDir):
		shutil.rmtree(dstDir)
	
	os.makedirs(dstDir)
	os.makedirs("temp")

	copy_tree(srcDir, "temp")
	os.system("cp " + sys.path[0]+"/bin/Makefile temp/Makefile")  # Prepare files
	os.system("cd temp && make libname="+targetName) # Compile and run

	copyHeaders("temp", dstDir)
	copyLibrary("temp", dstDir)

def exit_handler():
	print "Cleaning Up"
	clearTempFiles()

print(len(argv))

if len(argv) == 2:
	srcDir = argv[1]
	compileSource(srcDir,getLibraryName(srcDir), srcDir+"-compiled")
elif len(argv) == 3:
	srcDir = argv[1]
	targetName = argv[2]
	compileSource(srcDir,targetName, srcDir+"-compiled")
elif len(argv) > 3:
	srcDir = argv[1]
	targetName = argv[2]
	dstDir = argv[3]
	compileSource(srcDir,targetName, dstDir)
else:
	print("Error: Missing arguments")

atexit.register(exit_handler)