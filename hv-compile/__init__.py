#!/usr/bin/python

import shutil, errno, os, sys, utils
from sys import argv

tempDir = "temp"
binDir  = utils.getCurrentDirectory() + "/bin"

def compileSource(srcDir, targetName, dstDir):
	try:
		print("Compiling  '" + targetName + "' in " + srcDir)

		utils.removeDirectory(tempDir)
		utils.removeDirectory(dstDir)
		
		os.makedirs(dstDir)
		os.makedirs(tempDir)

		utils.copyDirectory(srcDir, tempDir) # Prepare files
		utils.copyDirectory(binDir, tempDir)

		os.system("cd " + tempDir + " && make libname="+targetName) # Compile and run

		utils.copyHeaders(tempDir, dstDir)
		utils.copyLibrary(tempDir, dstDir)

	finally:
		utils.removeDirectory(tempDir)


if __name__ == '__main__':
	if len(argv) == 2:
		srcDir = argv[1]
		compileSource(srcDir, utils.getLibraryName(srcDir), srcDir+"-compiled")
	elif len(argv) == 3:
		srcDir = argv[1]
		targetName = argv[2]
		compileSource(srcDir, targetName, srcDir+"-compiled")
	elif len(argv) > 3:
		srcDir = argv[1]
		targetName = argv[2]
		dstDir = argv[3]
		compileSource(srcDir, targetName, dstDir)
	else:
		print("Error: Missing arguments")
		sys.exit()