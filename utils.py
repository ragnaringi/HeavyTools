#!/usr/bin/python
import sys, os, contextlib, shutil, tempfile
import distutils.dir_util

def hvccPath():
    path = os.path.join(currentFileDirectory(), '.hvcc')
    if not os.path.exists(path):
        var = raw_input("Please enter the path to hvcc on your system: ")
        var = os.path.normpath(var)
        if var.endswith(('hvcc.py')):
            pass
        elif var.endswith(('hvcc')):
            var = os.path.join(var, 'hvcc.py')
        elif var.endswith(('hvcc/')):
            var = var[:-1]
            var = os.path.join(var, 'hvcc.py')
        else:
            raise ValueError("Path to hvcc not recognised. Please provide path to either root folder or hvcc.py")
            
        with open(path, "w") as text_file:
            text_file.write(var)

    return open(path, 'r').read().replace('\n', '')

def replaceOccurencesOfStringInFile(filePath, string, replacement):
    tempPath = os.path.join(os.path.dirname(filePath), "temp" + os.path.splitext(filePath)[1])
    os.rename(filePath, tempPath)
    
    with open(tempPath, "rt") as fin:
        with open(filePath, "wt") as fout:
            for line in fin:
                fout.write(line.replace(string, replacement))
                
    os.remove(tempPath)

# Extracts library name from a Heavy source directory
def getLibraryName(srcDir):
    file = [filename for filename in os.listdir(srcDir) if filename.startswith("Heavy_")][0]
    return (os.path.splitext(file)[0])

## File Utilities

def currentFilePath():
    return os.path.realpath(__file__)

def currentFileDirectory():
    return os.path.dirname(__file__)

def copy(from_file, to_file):
  shutil.copy2(from_file, to_file)

def copy_tree(from_dir, to_dir):
    distutils.dir_util.copy_tree(from_dir, to_dir)

def rmtree(directory):
    shutil.rmtree(directory)

# Note: python 3.2 has tempfile.TemporaryDirectory() 
# which does the same as this
@contextlib.contextmanager
def TemporaryDirectory():
    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)