#!/usr/bin/python

import os, argparse
from sys import argv
from src.code import compileSource
from src.utils import getLibraryName

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Creates a project to run Heavy source")
    parser.add_argument("input_dir",
        default = os.getcwd(),
        nargs='?',
        help = "A directory containing Heavy source. All .{h,hpp,c,cpp} files in the directory will be added to project.")
    parser.add_argument(
        "-n", "--name",
        nargs='?',
        help = "Name of the Heavy context. If none is provided, first one found will be used")
    parser.add_argument(
        "-o", "--out",
        nargs="?",
        help="List of destination directories for retrieved files.")
    
    
    args = parser.parse_args()

    if args.name is None:
        args.name = getLibraryName(args.input_dir).split('_')[1]

    if args.out is None:
        args.out = args.input_dir+"-compiled"

    compileSource(args.input_dir, args.name, args.out)