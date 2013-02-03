#!/usr/bin/env python2

import os
import sys
import subprocess
import time
from datetime import datetime
import psutil
import sensors

from config import *

CPUSENSOR = None

LASTSENT = None
LASTRECV = None
LASTTIMESTAMP = None

def get_cpu_freq():
    try:
        cpuinfo = open('/proc/cpuinfo', 'r')
        for l in cpuinfo.readlines():
            if l[:7] == 'cpu MHz':
                cpufreq = float(l.split(':')[1].strip())
                break

        cpuinfo.close()

        return cpufreq / 1000
    except:
        return 0.0

def get_cpu_temp():
    if CPUSENSOR:
        return CPUSENSOR.get_value()
    else:
        return 0.0

def get_uptime_and_load():
    res = subprocess.check_output(['uptime'])
    fields = res.strip().split()

    uptime = fields[0]
    load = (fields[7] + fields[8] + fields[9]).replace(',', ' ')

    return (uptime, load)

def get_gpu_temp():
    res = subprocess.check_output(['nvidia-settings', '-q', 'gpucoretemp'])
    temp = res.split('\n')[1].split(': ')[1].replace('.', '')

    return int(temp.strip())

def get_net_speed():
    global LASTTIMESTAMP, LASTRECV, LASTSENT

    eth0 = psutil.network_io_counters(pernic=True)['eth0']
    now = long(datetime.now().strftime('%s'))
    downspeed = 0.0
    upspeed = 0.0

    if LASTTIMESTAMP:
        downspeed = (eth0.bytes_recv - LASTRECV) / (now - LASTTIMESTAMP) / 1024.0
        upspeed = (eth0.bytes_sent - LASTSENT) / (now - LASTTIMESTAMP) / 1024.0

    LASTRECV = eth0.bytes_recv
    LASTSENT = eth0.bytes_sent
    LASTTIMESTAMP = now

    return (downspeed, upspeed)

def get_data():
    ret = " "

    cpu = psutil.cpu_percent(interval=0)
    cpufreq = get_cpu_freq()
    cputemp = get_cpu_temp()
    ret += title("cpu") + icon("cpu", fg=COLOR['MAGENTA2'])
    ret += text("%.2fGHz " % cpufreq)
    ret += progress(int(cpu), fg=COLOR['MAGENTA'])
    if cputemp > 60:
        ret += text("%dc" % int(cputemp), fg=COLOR['RED2'])
    else:
        ret += text("%dc" % int(cputemp))
    ret += sep()

    (uptime, load) = get_uptime_and_load()
    ret += title("load") + text("%s" % load)
    ret += sep()
    ret += title("uptime") + text("%s" % uptime)
    ret += sep()

    mem = psutil.virtual_memory().percent
    ret += title("mem") + icon("mem", fg=COLOR['GREEN2'])
    ret += progress(int(mem), fg=COLOR['GREEN2'])
    ret += sep()

    gputemp = get_gpu_temp()
    ret += title("gpu")
    if gputemp > 60:
        ret += text("%dc" % gputemp, fg=COLOR['RED2'])
    else:
        ret += text("%dc" % gputemp)
    ret += sep()

    disk = psutil.disk_usage('/').percent
    ret += title("disk") + icon("fs_01", fg=COLOR['YELLOW'])
    ret += progress(int(disk), fg=COLOR['YELLOW'])
    ret += sep()

    (downspeed, upspeed) = get_net_speed()
    ret += title("net")
    ret += icon("net_down_03", fg=COLOR['GREEN2'])
    ret += text("%.1f " % downspeed)
    ret += icon("net_up_03", fg=COLOR['RED2'])
    ret += text("%.1f " % upspeed)

    return ret

if __name__=="__main__":

    sensors.init()

    for chip in sensors.iter_detected_chips():
        for feature in chip:
            if feature.label[:4] == 'temp':
                CPUSENSOR = feature
                break

    args = [ "-x", "600",
             "-y", "0",
             "-w", "1120",
             "-h", str(HEIGHT),
             "-ta", "l",
             "-bg", COLOR['BG'],
             "-fg", COLOR['FG'],
             "-fn", FONT ]

    dzen = subprocess.Popen(['dzen2'] + args, stdin=subprocess.PIPE)

    while 1:
        dzen.stdin.write(get_data() + '\n')
        time.sleep(1)
