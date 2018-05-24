import shutil, os, sys
from sys import argv
from glob import glob
from os import path
from os.path import join
from distutils.dir_util import copy_tree

binDir = os.path.join(sys.path[0], "bin")

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


# Extracts library name from a Heavy source directory
def getLibraryName(srcDir):
    file = [filename for filename in os.listdir(srcDir) if filename.startswith("Heavy_")][0]
    return (os.path.splitext(file)[0])


def copyProjectFiles(dstDir, projectType):
    filePaths = []
    srcDir = join(binDir, sys.platform, projectType)
    files = os.listdir(srcDir)
    for file in files:
        if file == ".DS_Store": continue
        oldPath = join(srcDir,file)
        newPath = join(dstDir, file)
        copy(oldPath, newPath)
        filePaths.append(newPath)
    return filePaths


def renameProject(projectFiles, name):
    if not sys.platform == "darwin":
        raise NotImplementedError
    
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
    if not sys.platform == "darwin":
        raise NotImplementedError
    
    for file in projectFiles:
        newPath = file
        if os.path.splitext(file)[1] == ".xcodeproj":
            newPath = join(file, "project.pbxproj")
        replaceOccurencesOfStringInFile(newPath, "test", name)


def createProject(srcDir, name, projectType):
    try:
        # Copy project files
        projectFiles = copyProjectFiles(srcDir, projectType)

        # Rename project
        projectFiles = renameProject(projectFiles, name)

        # Edit file references references
        updateProjectFileReferences(projectFiles, name)

    finally:
        print("Project Created")


if __name__ == '__main__':
    srcDir = os.getcwd()
    targetName = getLibraryName(srcDir).split('_')[1]
    projectType = "c"

    if len(argv) > 1:
        targetName = argv[1]

    # TODO:
    # 1. Check how many contexts found in directory and
    #    ask to user to select if multiple are present
    # 2. Check for project type. Currently only Xcode
    #    command line C is supported
    # 3. Add option to precompile static lib
    #
    if not (sys.platform == "darwin"):
        print("Currently only supported on Mac OSX")
        raise NotImplementedError

    createProject(srcDir, targetName, projectType)
