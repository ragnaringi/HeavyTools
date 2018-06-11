#!/usr/bin/python

import utils, os, tempfile

tempDir = tempfile.mkdtemp(prefix="hv_compile-")
binDir  = utils.getCurrentDirectory() + "/../bin"

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
