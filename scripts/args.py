#!/usr/bin/python

import argparse, os

def default_args(desc=""):
    parser = argparse.ArgumentParser(
        description=desc)
    parser.add_argument("input_dir",
        default = os.getcwd(),
        nargs='?',
        help = "A directory containing a _main.pd file.")
    parser.add_argument(
        "-n", "--name",
        nargs='?',
        default="Test",
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

    return parser.parse_args()