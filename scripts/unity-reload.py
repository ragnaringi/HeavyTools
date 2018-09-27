#!/usr/bin/python

import os, sys, argparse, subprocess
import paths
import utils
from args import default_args

build = __import__("unity-build")

def run(input_dir, name, out_dir, noclean = 0):
    build.run(input_dir, name, out_dir, noclean)
    platform = sys.platform
    if platform == "darwin":
        subprocess.call("osascript -e 'activate application \"Unity\"' \
                                   -e 'tell application \"System Events\"' \
                                   -e 'keystroke \"p\" using {command down}' \
                                   -e 'end tell'", shell=True)
    else:
        print("Platform not supported yet")

if __name__ == "__main__":
    args = default_args("Builds Unity plugin for current platform and reloads Unity on completion")
    
    input_dir = args.input_dir
    name = args.name
    out_dir = args.out
    
    run(input_dir, name, out_dir, args.noclean)
