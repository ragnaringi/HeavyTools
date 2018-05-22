import shutil, os, sys
from distutils.dir_util import copy_tree


def getScriptPath():
  return os.path.dirname(os.path.realpath(sys.argv[0]))


def createProject(srcDir, targetName):
  try:
    copy_tree(os.path.join(sys.path[0], "bin", sys.platform, "c.xcodeproj"), os.path.join(srcDir, targetName + ".xcodeproj"))

    # Collect all source files and add to project
    

  finally:
    print("Project Created")


if __name__ == '__main__':
  # if len(argv) == 2:
    # srcDir = argv[1]
    # compileSource(srcDir, utils.getLibraryName(srcDir), srcDir+"-compiled")
  # elif len(argv) == 3:
    # srcDir = argv[1]
    # targetName = argv[2]
    # compileSource(srcDir, targetName, srcDir+"-compiled")
  # elif len(argv) > 3:
    # srcDir = argv[1]
    # targetName = argv[2]
    # dstDir = argv[3]
    # compileSource(srcDir, targetName, dstDir)
  # else:
    # print("Error: Missing arguments")
    # sys.exit()

  createProject(os.getcwd(), "metro")