#!/usr/bin/python

import os, signal, sys, argparse, subprocess, shutil, tempfile
import time
# import logging
from distutils.dir_util import copy_tree
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

sys.path.append("..")
from utils import hvccPath
from utils import replaceOccurencesOfStringInFile
hv_compile = __import__('hv-compile')
hv_project = __import__('hv-project')

input_dir = ""
name = ""
out_dir = ""
process = ""
postscript = None
clean = 0

class Event(LoggingEventHandler):
    
    run_process = None
    temp_compile_path = ""

    def cleanup(self):
        if os.path.exists(self.temp_compile_path):
            shutil.rmtree(self.temp_compile_path)
        if not self.run_process == None and self.run_process.poll() == None:
            os.killpg(self.run_process.pid, signal.SIGTERM)

    def dispatch(self, event):
        self.cleanup()

        filename, extension = os.path.splitext(event.src_path)
        print("Changes made to file: " + filename + extension)
        
        if not extension == ".pd":
            print("File is not of type '.pd'. Ignoring")
            return

        mainFile = os.path.join(args.input_dir, "_main.pd")
        
        if not os.path.exists(mainFile):
            print("No '_main.pd' found. Aborting.")
            return
            
        tempDir = tempfile.mkdtemp(prefix="hv_watchdog-")
        
        if process == "compile" or process == "build" or process == "run":
            print("Compiling source")
            self.temp_compile_path = tempfile.mkdtemp(prefix="hv_watchdog-")
            command = "python2.7 " + hvccPath() \
                    + " " + mainFile \
                    + " -n " + name \
                    + " -o " + self.temp_compile_path \
                    + " -g c-src"
            subprocess.call(command, shell=True)

            cSource = os.path.join(self.temp_compile_path, 'c')

            if process == "build":
                print("Building source")
                hv_compile.compileSource(cSource, name, tempDir)
            elif process == "run":
                print("Running source")
                hv_project.create(cSource, name, 'c')
                
                self.run_process = subprocess.Popen("python ../hv-run " + cSource, \
                                                    shell=True, \
                                                    preexec_fn=os.setsid)
            else:
                copy_tree(cSource, tempDir)
            
        elif process == "unity":
            print("Reloading Unity plugin")
            
            command = "python2.7 " + hvccPath() \
                    + " " + mainFile \
                    + " -n " + name \
                    + " -o " + tempDir \
                    + " -g unity"
            subprocess.call(command, shell=True)
            
            unitySource = os.path.join(tempDir, "unity", "source", "unity")
            
            # Copy AudioLib.cs template
            binDir = os.path.join(os.path.dirname(__file__), "bin")
            template = os.path.join(binDir, "Hv_Test_AudioLib.cs")
            newScript = os.path.join(unitySource, "Hv_" + name + "_AudioLib.cs")
            shutil.copy2(template, newScript)
            # Replace template context references with current patch name
            replaceOccurencesOfStringInFile(newScript, "Hv_Test", "Hv_" + name)
            replaceOccurencesOfStringInFile(newScript, "hv_Test", "hv_" + name)
            
            # TODO: Build
            
        if os.path.exists(out_dir) and clean:
            shutil.rmtree(out_dir)
        
        os.makedirs(out_dir)
        copy_tree(tempDir, out_dir)
        # shutil.rmtree(tempDir)
        print(tempDir)

        if not postscript is None:
            print("Running postscript: " + postscript)
            ext = os.path.splitext(postscript)[1]
            if ext == ".scpt":
                subprocess.call("osascript " + postscript, shell=True)
            elif ext == ".sh":
                subprocess.call("sh " + postscript, shell=True)
            elif ext == ".py":
                print("Running python script")
                subprocess.call("python " + postscript, shell=True)
            else:
                print("Script type not recognised: " + ext)

        print("[hv-watchdog] Process Complete")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Watches for '.pd' file modifications in a given directory and triggers a specified process on change")
    parser.add_argument("input_dir",
        default = os.getcwd(),
        nargs='?',
        help = "A directory containing a _main.pd file.")
    parser.add_argument(
        "-n", "--name",
        nargs='?',
        help = "Name of the Heavy patch or context. If none is provided an attempt will be made to automatically derive it")
    parser.add_argument(
        "-o", "--out",
        nargs="?",
        default=["./"], # by default
        help="List of destination directories for retrieved files.")
    parser.add_argument(
        "-c", "--clean",
        nargs="?",
        type=int,
        default=0,
        help="Specifies whether to clean output directory on new process")
    parser.add_argument(
        "-p", "--process",
        default = "compile",
        nargs='?',
        help = "Process to trigger on file changes")
    parser.add_argument(
        "-ps", "--postscript",
        nargs='?',
        help = "Specifies a script to run after process completes")
    
    args = parser.parse_args()

    if args.name is None:
        args.name = os.path.basename(args.input_dir) # Try to get name from root directory if none is provided

    input_dir = args.input_dir
    name = args.name
    out_dir = args.out
    clean = args.clean
    process = args.process
    postscript = args.postscript

    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = Event()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        event_handler.cleanup()

    observer.join()
