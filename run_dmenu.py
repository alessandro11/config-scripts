#!/usr/bin/env python2

import os
import sys
import subprocess

PATH = os.path.abspath(os.path.dirname(__file__))

from config import *

if __name__=="__main__":

    args = [ "-fn", FONT,
             "-nb", COLOR['BG'],
             "-nf", COLOR['FG'],
             "-sb", COLOR['BLACK'],
             "-sf", COLOR['CYAN'] ]

    dmenu = subprocess.Popen(['dmenu_run'] + args)
    dmenu.wait()
