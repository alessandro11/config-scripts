#!/usr/bin/env python2

import os
import sys
import subprocess
import time
from datetime import datetime
import psutil
import sensors
import re

class SysInfoDock:

    def __init__(self):
        if not 'FONT' in globals():
            raise Exception('Config not loaded, missing \'from config import *\'?')

        sensors.init()

        for chip in sensors.iter_detected_chips():
            for feature in chip:
                if feature.label[:4] == 'temp':
                    self.cpusensor = feature
                    break

        self.lastsent = None
        self.lastrecv = None
        self.lasttimestamp = None

        self.re_uptime = re.compile('^ .* up (?P<uptime>.*),  [0-9]* user,  load average: (?P<load>.*)$')

    def run(self):
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
            dzen.stdin.write(self.get_data() + '\n')
            time.sleep(1)

    def get_data(self):
        ret = " "

        cpu = psutil.cpu_percent(interval=0)
        cpufreq = self.get_cpu_freq()
        cputemp = self.get_cpu_temp()
        ret += title("cpu") + icon("cpu", fg=COLOR['MAGENTA2'])
        ret += text("%.2fGHz " % cpufreq)
        ret += progress(int(cpu), fg=COLOR['MAGENTA'])
        if cputemp > 60:
            ret += text("%dc" % int(cputemp), fg=COLOR['RED2'])
        else:
            ret += text("%dc" % int(cputemp))
        ret += sep()

        (uptime, load) = self.get_uptime_and_load()
        ret += title("load") + text("%s" % load)
        ret += sep()
        ret += title("uptime") + text("%s" % uptime)
        ret += sep()

        mem = psutil.virtual_memory().percent
        ret += title("mem") + icon("mem", fg=COLOR['GREEN2'])
        ret += progress(int(mem), fg=COLOR['GREEN2'])
        ret += sep()

        gputemp = self.get_gpu_temp()
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

        (downspeed, upspeed) = self.get_net_speed()
        ret += title("net")
        ret += icon("net_down_03", fg=COLOR['GREEN2'])
        ret += text("%.1f " % downspeed)
        ret += icon("net_up_03", fg=COLOR['RED2'])
        ret += text("%.1f " % upspeed)

        return ret
    def get_cpu_freq(self):
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

    def get_cpu_temp(self):
        if self.cpusensor:
            return self.cpusensor.get_value()
        else:
            return 0.0

    def get_uptime_and_load(self):
        res = self.re_uptime.match(subprocess.check_output(['uptime']))

        uptime = res.group('uptime')
        load = res.group('load').replace(',', '')

        return (uptime, load)

    def get_gpu_temp(self):
        res = subprocess.check_output(['nvidia-settings', '-q', 'gpucoretemp'])
        temp = res.split('\n')[1].split(': ')[1].replace('.', '')

        return int(temp.strip())

    def get_net_speed(self):
        eth0 = psutil.network_io_counters(pernic=True)['eth0']
        now = long(datetime.now().strftime('%s'))
        downspeed = 0.0
        upspeed = 0.0

        if self.lasttimestamp:
            downspeed = (eth0.bytes_recv - self.lastrecv) / (now - self.lasttimestamp) / 1024.0
            upspeed = (eth0.bytes_sent - self.lastsent) / (now - self.lasttimestamp) / 1024.0

        self.lastrecv = eth0.bytes_recv
        self.lastsent = eth0.bytes_sent
        self.lasttimestamp = now

        return (downspeed, upspeed)


if __name__=="__main__":
    PATH = os.path.abspath(os.path.dirname(__file__) + "/../")
    sys.path.append(PATH)

    from config import *

    dock = SysInfoDock()
    dock.run()
