#!/usr/bin/python

import sys, os, subprocess, shutil, tempfile
from distutils.dir_util import copy_tree
from sys import argv

sys.path.append(os.path.join(sys.path[0], ".."))
hv_project = __import__('hv-project')

tempDir = tempfile.mkdtemp(prefix="hv_run-")

def clearTempFiles():
    if os.path.exists(tempDir):
        shutil.rmtree(tempDir)

def processPatch(srcDir, name, type):
    try:
        print("Compiling: " + srcDir)
        # Prepare temporary directory
        clearTempFiles()
        os.makedirs(tempDir)

        if type == 1:
            subprocess.call("hv-uploader " + srcDir + " -n " + name + " -o " + tempDir + " -g c-src", shell=True) # Upload
        else: 
            # Directory is heavy source
            copy_tree(srcDir, tempDir)

        # Create project to run
        hv_project.create(tempDir, name, "c")

        # Compile and run project
        os.system("cd " + tempDir + " && make && ./main") # Compile and run
    finally:
        clearTempFiles()
