#!/usr/bin/python

import argparse
from hv-projectgenerator import generateProject, getLibraryName

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
    
    args = parser.parse_args()
    
    if args.name is None:
        args.name = getLibraryName(args.input_dir).split('_')[1]
        
    # TODO:
    # 1. Check how many contexts found in directory and
    #    ask user to select if multiple are present
    # 2. Add option to precompile static lib
    #
    
    createProject(args.input_dir, args.name, args.type)
