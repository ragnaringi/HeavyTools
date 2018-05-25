#!/usr/bin/python

import shutil, os, sys, argparse
from sys import argv
from glob import glob
from os import path
from os.path import join
from distutils.dir_util import copy_tree

binDir = os.path.join(os.path.join(os.path.dirname(__file__), os.pardir), "bin")

def copy(srcPath, dstPath):
    if os.path.isdir(srcPath):
        copy_tree(srcPath, dstPath)
    else:
        shutil.copy2(srcPath, dstPath)


def getScriptPath():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def getFilesWithExtension(srcDir, extensions):
    files = []
    for ext in extensions:
        files.extend(glob(join(srcDir, ext)))
    return files


def replaceOccurencesOfStringInFile(filePath, string, replacement):
    tempPath = join(path.dirname(filePath), "temp" + path.splitext(filePath)[1])
    os.rename(filePath, tempPath)
    
    with open(tempPath, "rt") as fin:
        with open(filePath, "wt") as fout:
            for line in fin:
                fout.write(line.replace(string, replacement))
                
    os.remove(tempPath)
    

def copyProjectFiles(dstDir, projectType):
    filePaths = []
    srcDir = join(binDir, projectType)
    if not path.exists(srcDir):
        raise ValueError("Project type : " + projectType + " doesn't exist")
        
    files = os.listdir(srcDir)
    for file in files:
        if file == ".DS_Store": continue
        oldPath = join(srcDir,file)
        newPath = join(dstDir, file)
        copy(oldPath, newPath)
        filePaths.append(newPath)
    return filePaths


def renameProject(projectFiles, name):
    filePaths = []
    
    for file in projectFiles:
        newPath = file
        extension = os.path.splitext(file)[1]
        if extension == ".xcodeproj":
            newPath = join(path.dirname(file), name + extension)
            if path.exists(newPath):
                shutil.rmtree(newPath)
            os.rename(file, newPath)
            
        filePaths.append(newPath)
    
    return filePaths


def updateProjectFileReferences(projectFiles, name):
    for file in projectFiles:
        newPath = file
        if os.path.splitext(file)[1] == ".xcodeproj":
            newPath = join(file, "project.pbxproj")
        replaceOccurencesOfStringInFile(newPath, "test", name)


def create(srcDir, name, projectType):
    try:
        # Copy project files
        projectFiles = copyProjectFiles(srcDir, projectType)
        
        # Rename project
        projectFiles = renameProject(projectFiles, name)
        
        # Edit file references references
        updateProjectFileReferences(projectFiles, name)
        
    finally:
        print("Project Created")

def rename(srcDir, name):
    raise NotImplementedError

def clean(srcDir):
    raise NotImplementedError
