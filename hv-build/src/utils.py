#!/usr/bin/python

import shutil, errno, os
from glob import glob
from os.path import join
from distutils.dir_util import copy_tree


def removeDirectory(dir):
	if os.path.exists(dir):
		shutil.rmtree(dir)


def copyDirectory(src, dst):
	copy_tree(src, dst)


def getCurrentDirectory():
	return os.path.dirname(os.path.abspath(__file__))


def getFilesWithExtension(srcDir, extensions):
	files = []
	for ext in extensions:
		files.extend(glob(join(srcDir, ext)))
	return files


def getLibraryName(srcDir):
	file = [filename for filename in os.listdir(srcDir) if filename.startswith("Heavy_")][0]
	return (os.path.splitext(file)[0])


def copyHeaders(srcDir, dstDir):
	for file in getFilesWithExtension(srcDir,('*.h', '*.hpp')):
		if os.path.isfile(file):
			shutil.copy2(file, dstDir)


def copyLibrary(srcDir, dstDir):
	for file in getFilesWithExtension(srcDir,('*.a', '*.so')):
		if os.path.isfile(file):
			shutil.copy2(file, dstDir)