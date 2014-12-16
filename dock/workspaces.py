#!/usr/bin/env python2

import os
import sys
import subprocess

PATH = os.path.abspath(os.path.dirname(__file__) + "/../")
sys.path.append(PATH)

from config import *

if __name__=="__main__":

    args = [ "-x", "0",
             "-y", "0",
             "-w", DOCK_POS['WSw'],
             "-h", str(HEIGHT),
             "-ta", "l",
             "-bg", COLOR['BG'],
             "-fg", COLOR['FG'],
             "-fn", FONT ]

    dzen = subprocess.Popen(['dzen2'] + args, stdin=sys.stdin)
    sys.exit(dzen.wait())
