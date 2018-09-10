import os, sys, argparse, subprocess, shutil, tempfile
import time
# import logging
from distutils.dir_util import copy_tree
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

sys.path.append("..")
from utils import hvccPath
from utils import replaceOccurencesOfStringInFile
hv_compile = __import__('hv-compile')

input_dir = ""
name = ""
out_dir = ""
process = ""
extra = ""
clean = 0

class Event(LoggingEventHandler):
    def dispatch(self, event):
        filename, extension = os.path.splitext(event.src_path)
        print("Changes made to file: " + filename + extension)
        if extension == ".pd":
            mainFile = os.path.join(args.input_dir, "_main.pd")
            if os.path.exists(mainFile):
                
                tempDir = tempfile.mkdtemp(prefix="hv_watchdog-")
                
                if process == "compile" or "build" or "run":
                    print("Compiling source")
                    compileTemp = tempfile.mkdtemp(prefix="hv_watchdog-")
                    command = "python2.7 " + hvccPath() \
                            + " " + mainFile \
                            + " -n " + name \
                            + " -o " + compileTemp \
                            + " -g c-src"
                    subprocess.call(command, shell=True)
                    
                    cSource = os.path.join(compileTemp, 'c')
                    
                    if process == "build":
                        print("Building source")
                        hv_compile.compileSource(cSource, name, tempDir)
                    elif process == "run":
                        print("Running source")
                    else:
                        copy_tree(cSource, tempDir)
                    
                    shutil.rmtree(compileTemp)
                    
                elif process == "unity":
                    print("Reloading Unity plugin")
                    # Download Unity binary
                    binaryFlag = "unity-macos-x64"
                    if sys.platform.startswith('win'):
                        binaryFlag = "unity-win-x64"
                    elif sys.platform.startswith('lin'):
                        binaryFlag = "unity-linux-x64"
                    
                    command = "python2.7 " + hvccPath() \
                            + " " + mainFile \
                            + " -n " + name \
                            + " -o " + tempDir \
                            + " -g " + binaryFlag
                    subprocess.call(command, shell=True)
                    
                    # Copy AudioLib.cs template
                    binDir = os.path.join(os.path.dirname(__file__), "bin")
                    tempFile = os.path.join(tempDir, "Hv_" + name + "_AudioLib.cs")
                    shutil.copy2(os.path.join(binDir, "Hv_Test_AudioLib.cs"), tempFile)
                    # Replace template context references with current patch name
                    replaceOccurencesOfStringInFile(tempFile, "Hv_Test", "Hv_" + name)
                    replaceOccurencesOfStringInFile(tempFile, "hv_Test", "hv_" + name)
                    
                if os.path.exists(out_dir) and clean:
                    shutil.rmtree(out_dir)
                
                os.makedirs(out_dir)
                copy_tree(tempDir, out_dir)
                shutil.rmtree(tempDir)
                print("[hv-watchdog] Process Complete")
                
                # If specified, we trigger Unity to play automatically
                if process == "unity" and extra == "restart":
                    if sys.platform == "darwin":
                        binDir = os.path.join(os.path.dirname(__file__), "bin")
                        subprocess.call("osascript " + os.path.join(binDir, "RunUnity.scpt"), shell=True)
                    else:
                        print("Restarting the Editor is only supported on MacOS")
            else:
                print("No '_main.pd' found. Aborting.")
        else:
            print("File is not of type '.pd'. Ignoring")


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
        "-e", "--extra",
        nargs='?',
        help = "Extra Post-Process info")
    
    args = parser.parse_args()

    if args.name is None:
        args.name = os.path.basename(args.input_dir) # Try to get name from root directory if none is provided

    input_dir = args.input_dir
    name = args.name
    out_dir = args.out
    clean = args.clean
    process = args.process
    extra = args.extra

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
