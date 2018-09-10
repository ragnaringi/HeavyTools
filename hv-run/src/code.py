#!/usr/bin/python

import sys, os, subprocess, shutil, tempfile
from distutils.dir_util import copy_tree

sys.path.append(sys.path[0])
from utils import hvccPath

sys.path.append(os.path.join(sys.path[0], ".."))
hv_project = __import__('hv-project')

tempDir = tempfile.mkdtemp(prefix="hv_run-")

def clearTempFiles():
    if os.path.exists(tempDir):
        shutil.rmtree(tempDir)

def processPatch(srcDir, name, type):
    try:
        print("Compiling: " + srcDir)
        clearTempFiles()
        os.makedirs(tempDir)

        if type == 1:
            command = "python2.7 " + hvccPath() \
                    + " " + os.path.join(srcDir, '_main.pd') \
                    + " -n " + name \
                    + " -o " + tempDir \
                    + " -g c-src"
            subprocess.call(command, shell=True)
        else: 
            # Directory is heavy source
            copy_tree(srcDir, os.path.join(tempDir, 'c'))

        # Create project to run
        cSource = os.path.join(tempDir, 'c')
        hv_project.create(cSource, name, 'c')

        # Compile and run project
        os.system("cd " + cSource + " && make && ./main")
    finally:
        clearTempFiles()
