#!/usr/bin/python

import os, subprocess, args, paths, utils
from utils import hvccPath
from utils import replaceOccurencesOfStringInFile

def run(input_dir, name, out_dir, noclean=0):
    print("Compiling Unity plugin")
    
    with utils.TemporaryDirectory() as temp_dir:
        mainFile = os.path.join(input_dir, "_main.pd")
        
        command = "python2.7 " + hvccPath() \
                + " " + mainFile \
                + " -n " + name \
                + " -o " + temp_dir \
                + " -g unity"
        subprocess.call(command, shell=True)
        
        unitySource = os.path.join(temp_dir, "unity", "source", "unity")
        
        # TODO: This stage can be replaced by updaint AudioLib.cs template in hvcc
        # Copy AudioLib.cs template
        template = os.path.join(os.path.dirname(__file__), "..", "static", "Hv_Test_AudioLib.cs")
        newScript = os.path.join(unitySource, "Hv_" + name + "_AudioLib.cs")
        utils.copy(template, newScript)
        # Replace template context references with current patch name
        replaceOccurencesOfStringInFile(newScript, "Hv_Test", "Hv_" + name)
        replaceOccurencesOfStringInFile(newScript, "hv_Test", "hv_" + name)
        
        if os.path.exists(out_dir) and not noclean:
            utils.rmtree(out_dir)
            
        utils.copy_tree(os.path.join(temp_dir, "unity"), out_dir)


if __name__ == "__main__":
    args = args.default_args("Compiles a Pd patch to Unity source")
    
    input_dir = args.input_dir
    name = args.name
    out_dir = args.out
    
    run(input_dir, name, out_dir, args.noclean)
