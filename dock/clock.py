#!/usr/bin/env python2

import os
import sys
import subprocess
import time

import config

if __name__=="__main__":

    fmt = '%d^fg(#444).^fg()%m^fg(#444).^fg()%Y^fg(#007b8c)/^fg(#5f656b)%a ^fg(#a488d9)| ^fg()%H^fg(#444):^fg()%M^fg(#444):^fg()%S'

    args = [ "-x", "1720",
             "-y", "0",
             "-w", "200",
             "-h", str(config.HEIGHT),
             "-ta", "r",
             "-bg", config.COLOR['BG'],
             "-fg", config.COLOR['FG'],
             "-fn", config.FONT ]

    dzen = subprocess.Popen(['dzen2'] + args, stdin=subprocess.PIPE)

    while 1:
        #dzen.stdin.write(dock.format_arrows())
        dzen.stdin.write(time.strftime(fmt) + ' \n')
        time.sleep(1)
