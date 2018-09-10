#!/usr/bin/python
import sys, os

def hvccPath():
    path = os.path.join(currentFileDirectory(), '.hvcc')
    if not os.path.exists(path):
        print "ERROR: File does not exist"
    return open(path, 'r').read().replace('\n', '')

def currentFilePath():
    return os.path.realpath(__file__)

def currentFileDirectory():
    return os.path.dirname(__file__)

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