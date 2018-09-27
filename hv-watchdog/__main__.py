#!/usr/bin/python

import os, signal, sys, argparse, subprocess, shutil
import time
from distutils.dir_util import copy_tree
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

sys.path.append("..")
import utils
from utils import hvccPath
from utils import replaceOccurencesOfStringInFile

input_dir = ""
name = ""
out_dir = ""
process = ""
postscript = None
noclean = 0

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
        
        if not os.path.exists(os.path.join(input_dir, "_main.pd")):
            print("No '_main.pd' found. Aborting.")
            return
            
        if not os.path.exists(postscript):
            print("Post script not found. Aborting.")
            return
            
        subprocess.call("python " + postscript + " " + input_dir + " -n" + name + " -o" + out_dir + " --noclean " + str(noclean), shell=True)
        
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
        "-nc", "--noclean",
        nargs="?",
        type=int,
        default=0,
        help="Specifies whether to clean output directory on new process")
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
    noclean = args.noclean
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
