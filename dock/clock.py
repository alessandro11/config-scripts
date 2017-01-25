#!/usr/bin/env python2

import os
import sys
import subprocess
import time

PATH = os.path.abspath(os.path.dirname(__file__) + "/../")
sys.path.append(PATH)

from config import *

if __name__=="__main__":

    change_color = 1

    fmt = '^fg(#5f656b)%a ^fg(#007b8c)%d ^fg()%h^fg(#444) ^fg()%Y^fg(#007b8c) ^fg(#a488d9)| ^fg()%H^fg(#444):^fg()%M^fg(#444):^fg()%S'
    args = [ "-x", DOCK_POS['CLx'],
             "-y", "0",
             "-w", DOCK_POS['CLw'],
             "-h", str(HEIGHT),
             "-ta", "r",
             "-bg", COLOR['BG'],
             "-fg", COLOR['FG'],
             "-fn", FONT ]

    dzen = subprocess.Popen(['dzen2'] + args, stdin=subprocess.PIPE)

    while 1:
        dzen.stdin.write(arrows() + time.strftime(fmt) + ' \n')
        time.sleep(1)
        if change_color == True:
            color = '#ffffffff'
        else:
            color = '#444'
        change_color = ~change_color
        fmt = '^fg(#5f656b)%a ^fg(#007b8c)%d ^fg()%h^fg(#444) ^fg()%Y^fg(#007b8c) ^fg(#a488d9)| ^fg()%H^fg(' + color + '):^fg()%M^fg(' + color + '):^fg()%S'
