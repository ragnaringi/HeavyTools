#!/usr/bin/python

import os, sys, shutil, subprocess, argparse, json
import paths
import utils
from args import default_args

compile = __import__("unity-compile")

def json_data(file_path):
    data = None
    with open(file_path) as file:
        data = json.load(file)
    return data

def build_macosx(input_dir, name, out_dir):
    print("Building Unity Mac plugin")
    json = json_data(os.path.join(input_dir, "build.json"))["macos"]["x64"]
    projectDir = os.path.join(input_dir, json["projectDir"][0])
    
    # Check whether AudioPlugin already exists at destination
    # It should not have changed so we don't need to recompile
    pluginPath = os.path.join(out_dir, "AudioPlugin_Hv_" + name + ".bundle")
    targets = "" if os.path.exists(pluginPath) else "-alltargets"
    
    # Build
    subprocess.call("cd " + projectDir + " && xcodebuild " + targets, shell=True, stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT) 
    # Copy plugin to output dir
    buildDir = os.path.join(input_dir, *json["binaryDir"])
    utils.copy_tree(buildDir, out_dir)

def run(input_dir, name, out_dir, noclean = 0):
    with utils.TemporaryDirectory() as temp_dir:
        compile.run(input_dir, name, temp_dir)
        
        if os.path.exists(out_dir) and not noclean:
            shutil.rmtree(out_dir)

        print("Building Unity plugin binary")

        platform = sys.platform
        if platform == "darwin":
            build_macosx(temp_dir, name, out_dir)
        else:
            print("Platform not supported yet")


if __name__ == "__main__":
    args = default_args("Builds Unity plugin for current platform")
    
    input_dir = args.input_dir
    name = args.name
    out_dir = args.out
    
    run(input_dir, name, out_dir, args.noclean)
