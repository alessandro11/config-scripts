#!/usr/bin/env python2

import os
import sys
import subprocess
import time

PATH = os.path.abspath(os.path.dirname(__file__) + "/../")
sys.path.append(PATH)

from config import *

if __name__=="__main__":

    fmt = '%d^fg(#444).^fg()%m^fg(#444).^fg()%Y^fg(#007b8c)/^fg(#5f656b)%a ^fg(#a488d9)| ^fg()%H^fg(#444):^fg()%M^fg(#444):^fg()%S'

    args = [ "-x", "1150",
             "-y", "0",
             "-w", "220",
             "-h", str(HEIGHT),
             "-ta", "r",
             "-bg", COLOR['BG'],
             "-fg", COLOR['FG'],
             "-fn", FONT ]

    dzen = subprocess.Popen(['dzen2'] + args, stdin=subprocess.PIPE)

    while 1:
        dzen.stdin.write(arrows() + time.strftime(fmt) + ' \n')
        time.sleep(1)
