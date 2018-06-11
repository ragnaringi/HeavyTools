import os, sys, argparse, subprocess, shutil, tempfile
import time
# import logging
from distutils.dir_util import copy_tree
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

sys.path.append("..")

hv_compile = __import__('hv-compile')

input_dir = ""
name = ""
out_dir = ""
process = ""
clean = 0

class Event(LoggingEventHandler):
    def dispatch(self, event):
        filename, extension = os.path.splitext(event.src_path)
        print("Changes made to file: " + filename + extension)
        if extension == ".pd":
            print("Recompiling")
            if os.path.exists(os.path.join(args.input_dir, "_main.pd")):
                print("_main.pd exists")

                tempDir = tempfile.mkdtemp(prefix="hv_watchdog-")
                print("Uploading source")
                subprocess.call("hv-uploader " + input_dir + " -n " + name + " -o " + tempDir + " -g c-src", shell=True) # Upload
                
                if process == "compile":
                    print("Compiling source")
                    compileTemp = tempfile.mkdtemp(prefix="hv_watchdog-")
                    copy_tree(tempDir, compileTemp)
                    shutil.rmtree(tempDir)
                    hv_compile.compileSource(compileTemp, name, tempDir)
                    shutil.rmtree(compileTemp)
                elif process == "run":
                    print("TODO: Running source")
                elif process == "unity":
                    print("TODO: Reloading Unity plugin")

                if os.path.exists(out_dir):
                    if clean: 
                        shutil.rmtree(out_dir)
                else:
                    os.makedirs(out_dir)

                copy_tree(tempDir, out_dir)
                shutil.rmtree(tempDir)
                print("[hv-watchdog] Process Complete")
            else:
                print("No '_main.pd' found. Aborting.")
        else:
            print("File is not of type '.pd'. Ignoring")


# Extracts library name from a Heavy source directory
def getLibraryName(srcDir):
    file = [filename for filename in os.listdir(srcDir) if filename.startswith("Heavy_")][0]
    return (os.path.splitext(file)[0])

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
        "-p", "--process",
        default = "Upload",
        nargs='?',
        help = "Process to trigger on file changes")
    parser.add_argument(
        "-c", "--clean",
        nargs="?",
        type=int,
        default=0,
        help="Specifies whether to clean output directory on new process")
    
    args = parser.parse_args()

    if args.name is None:
        args.name = os.path.basename(args.input_dir) # Try to get name from root directory if none is provided

    input_dir = args.input_dir
    name = args.name
    out_dir = args.out
    process = args.process
    clean = args.clean

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
    observer.join()