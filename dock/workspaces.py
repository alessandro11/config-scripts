#!/usr/bin/env python2

import os
import sys
import subprocess

import config

if __name__=="__main__":

    args = [ "-x", "0",
             "-y", "0",
             "-w", "600",
             "-h", str(config.HEIGHT),
             "-ta", "l",
             "-bg", config.COLOR['BG'],
             "-fg", config.COLOR['FG'],
             "-fn", config.FONT ]

    dzen = subprocess.Popen(['dzen2'] + args, stdin=sys.stdin)
    sys.exit(dzen.wait())
