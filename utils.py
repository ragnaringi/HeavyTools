#!/usr/bin/python
import sys, os

def hvccPath():
    path = os.path.join(currentFileDirectory(), '.hvcc')
    if not os.path.exists(path):
        print "ERROR: File does not exist"
    return open(path, 'r').read().replace('\n', '')

def currentFilePath():
    return os.path.realpath(__file__)

def currentFileDirectory():
    return os.path.dirname(__file__)