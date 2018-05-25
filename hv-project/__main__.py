#!/usr/bin/python

import argparse, os
from src.code import create, rename, clean

# Extracts library name from a Heavy source directory
def getLibraryName(srcDir):
    file = [filename for filename in os.listdir(srcDir) if filename.startswith("Heavy_")][0]
    return (os.path.splitext(file)[0])

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
        "-t", "--type",
        default = "c",
        nargs='?',
        help="Project type. Default is 'c'")
    
    # TODO: Add options for rename and clean
    
    args = parser.parse_args()
    
    if args.name is None:
        args.name = getLibraryName(args.input_dir).split('_')[1]
        
    # TODO:
    # 1. Check how many contexts found in directory and
    #    ask user to select if multiple are present
    # 2. Add option to precompile static lib
    #
    
    create(args.input_dir, args.name, args.type)
