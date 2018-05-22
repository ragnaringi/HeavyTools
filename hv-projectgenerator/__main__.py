import shutil, os, sys
from sys import argv
from glob import glob
from os import path
from os.path import join
from distutils.dir_util import copy_tree

binDir = os.path.join(sys.path[0], "bin")

def getScriptPath():
  return os.path.dirname(os.path.realpath(sys.argv[0]))


def getFilesWithExtension(srcDir, extensions):
  files = []
  for ext in extensions:
    files.extend(glob(join(srcDir, ext)))
  return files


# Extracts library name from a Heavy source directory
def getLibraryName(srcDir):
  file = [filename for filename in os.listdir(srcDir) if filename.startswith("Heavy_")][0]
  return (os.path.splitext(file)[0])


def copyProjectFiles(dstDir, projectType):
  projectPath = join(binDir, sys.platform, projectType)
  copy_tree(projectPath, dstDir)


def renameProject(projectPath, name):
  if sys.platform == "darwin":
    newPath = join(path.dirname(projectPath), name + ".xcodeproj")
    if path.exists(newPath):
      shutil.rmtree(newPath)
    os.rename(projectPath, newPath)
  else:
    raise NotImplementedError
  
  return newPath


def updateProjectFileReferences(projectPath, name):
  if sys.platform == "darwin":
    filePath = join(projectPath, "project.pbxproj")
    replaceOccurencesOfStringInFile(filePath, "test", name)
  else:
    raise NotImplementedError


def replaceOccurencesOfStringInFile(filePath, string, replacement):
  tempPath = join(path.dirname(filePath), "temp" + path.splitext(filePath)[1])
  os.rename(filePath, tempPath)

  with open(tempPath, "rt") as fin:
    with open(filePath, "wt") as fout:
      for line in fin:
        fout.write(line.replace(string, replacement))

  os.remove(tempPath)


def createProject(srcDir, name, projectType):
  try:
    # Copy project
    copyProjectFiles(srcDir, projectType)

    # Rename project
    projectPath = renameProject(join(srcDir, projectType + ".xcodeproj"), name)

    # Edit project file references
    updateProjectFileReferences(projectPath, name)

    # Edit source files references
    mainFile = join(srcDir, "main." + projectType)
    replaceOccurencesOfStringInFile(mainFile, "test", name)

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
  #
  if not (sys.platform == "darwin"):
    print("Currently only supported on Mac OSX")
    raise NotImplementedError

  createProject(srcDir, targetName, projectType)
