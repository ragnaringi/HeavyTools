import os, shutil
from setup import downloadSource

print("Testing hv-compile")

srcPath = "src"
dstPath = "out"
name    = "metro"
libName = "libmetro.a"

if not os.path.exists(srcPath):
  print("Downloading test source files")
  downloadSource()

import sys
sys.path.append("..")
module = __import__('hv-compile')

print("Compiling '" + libName + "'")
module.compileSource(srcPath, name, dstPath)

if os.path.exists(os.path.join(dstPath,libName)):
  print("SUCCESS")
else:
  print("Compilation ERROR")

print("Cleaning Up")
shutil.rmtree(dstPath)
