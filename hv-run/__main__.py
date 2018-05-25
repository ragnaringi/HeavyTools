#!/usr/bin/python

import os, argparse
from src.code import processPatch

# Extracts library name from a Heavy source directory
def getLibraryName(srcDir):
    file = [filename for filename in os.listdir(srcDir) if filename.startswith("Heavy_")][0]
    return (os.path.splitext(file)[0])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Compiles and runs Pd patch or Heavy source")
    parser.add_argument("input_dir",
        default = os.getcwd(),
        nargs='?',
        help = "A directory containing Heavy source or a _main.pd file.")
    parser.add_argument(
        "-n", "--name",
        nargs='?',
        help = "Name of the Heavy patch or context. If none is provided an attempt will be made to automatically derive it")
    parser.add_argument(
        "-t", "--type",
        nargs='?',
        type = int,
        help = "Source type hint. Pass 0 for Heavy Source and 1 for Pd")
    
    args = parser.parse_args()
    
    if args.type is None:
        args.type = int(os.path.exists(os.path.join(args.input_dir, "_main.pd")))

    if args.name is None:
        if args.type == 0:
            args.name = getLibraryName(args.input_dir).split('_')[1]
        else:
            args.name = os.path.basename(args.input_dir) # If Pd source get name from root directory
        
    processPatch(args.input_dir, args.name, args.type)
