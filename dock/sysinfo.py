#!/usr/bin/env python2

import os
import sys
import subprocess
import time
from datetime import datetime
import psutil
import sensors
import re
import netifaces

class SysInfoDock:

    def __init__(self):
        if not 'FONT' in globals():
            raise Exception('Config not loaded, missing \'from config import *\'?')

        sensors.init()

        for chip in sensors.iter_detected_chips():
            for feature in chip:
                self.cpusensor = feature
                break

        self.lastsent = 0
        self.lastrecv = 0
        self.lasttimestamp = None
        self.blink_batt = True
        self.refresh_batt_left_in = 0
        self.time_batt_remaining = 0
        self.re_cpufreq = re.compile('^cpu .*(?P<tst> \d+\.\d*)$', re.M|re.I)

    def run(self):
        args = [ "-x", DOCK_POS['SIx'],
                 "-y", "0",
                 "-w", DOCK_POS['SIw'],
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
        
        ret += sep()
        ret += self.get_caps_lock()
        ret += sep()

        cpu = psutil.cpu_percent(interval=0)
        cpufreq = self.get_cpu_freq()
        cputemp = self.get_cpu_temp()
        ret += icon("cpu", fg=COLOR['MAGENTA2'])
        ret += text("%.2fGHz " % cpufreq)
        ret += progress(int(cpu), fg=COLOR['MAGENTA'])
        if cputemp > 60:
            ret += text("%dc" % int(cputemp), fg=COLOR['RED'])
        else:
            ret += text("%dc" % int(cputemp))
        ret += sep()

        (uptime, load) = self.get_uptime_and_load()
        ret += title("ld") + text("%s" % load)
        ret += sep()
        ret += title("up") + text("%s" % uptime)
        ret += sep()

        mem = psutil.virtual_memory().percent
        ret += icon("mem", fg=COLOR['GREEN'])
        ret += progress(int(mem), fg=COLOR['GREEN'])
        ret += sep()

#        gputemp = self.get_gpu_temp()
#        ret += title("gpu")
#        if gputemp > 60:
#            ret += text("%dc" % gputemp, fg=COLOR['RED2'])
#        else:
#            ret += text("%dc" % gputemp)
#        ret += sep()

        if BATT_PLUGGED:
            ret += self.get_batt_status()
        else:
            disk = psutil.disk_usage('/').percent
            ret += icon("fs_01", fg=COLOR['YELLOW'])
            ret += progress(int(disk), fg=COLOR['YELLOW'])

        
        self.iface = netifaces.gateways()['default']
        if len(self.iface) > 0:
            self.iface = self.iface[netifaces.AF_INET][1]
            ret += sep()
            (downspeed, down_unit, upspeed, up_unit) = self.get_net_speed()
            if self.iface == "enp6s0":
                icon_name = "net_wired"
            elif self.iface == "wlp3s0":
                icon_name = "wifi_02"
            else:
                icon_name = "net-wired2"

            icon_color = COLOR['GREY']
            icon_color_down = COLOR['GREEN2']
            icon_color_up = COLOR['RED2']
            if downspeed > 0.0 or upspeed > 0.0:
                icon_color = COLOR['GREEN']
                if downspeed > 0.0:
                    icon_color_down = COLOR['GREEN']
                if upspeed > 0.0:
                    icon_color_up = COLOR['RED']

            ret += icon(icon_name, icon_color)
            ret += icon("net_down_03", fg=icon_color_down)
            ret += text("%.1f%s " % (downspeed, down_unit))
            ret += icon("net_up_03", fg=icon_color_up)
            ret += text("%.1f%s " % (upspeed, up_unit))

        return ret

    def get_caps_lock(self):
        caps = subprocess.check_output(['xset', 'q'])
        caps = caps[caps.find('Caps Lock')+len('Caps Lock:'):].lstrip()
        caps = caps[:caps.find(' ')]
        ret = ''
        if caps == 'off':
            ret = title('caps')
        else:
            ret = text('CAPS', COLOR['GREEN'])

        return ret

    def get_cpu_freq(self):
        try:
            fd_cpuinfo = open('/proc/cpuinfo', 'r')
            buff = fd_cpuinfo.read()
            fd_cpuinfo.close()
            cpufreqs = self.re_cpufreq.findall(buff)
            sum_freq = 0.0
            count = 0
            for freq in cpufreqs :
                sum_freq = sum_freq + float(freq.strip())
                count = count + 1

            return (sum_freq / count) / 1000

        except:
            return 0.0

    def get_cpu_temp(self):
        if self.cpusensor:
            return self.cpusensor.get_value()
        else:
            return 0.0

    def get_uptime_and_load(self):
        str_uptime = subprocess.check_output(['uptime'])
        tmp = str_uptime[str_uptime.find('up')+3:]
        tmp = tmp[:tmp.find('user')]
        uptime = tmp[:tmp.rfind(',')]
        tmp = str_uptime[str_uptime.rfind('average:'):-1].split(' ')
        load = tmp[1][:-1] + ' ' + tmp[2][:-1] + ' ' + tmp[3]
        return(uptime, load)

    def get_gpu_temp(self):
        res = subprocess.check_output(['nvidia-settings', '-q', 'gpucoretemp'])
        temp = res.split('\n')[1].split(': ')[1].replace('.', '')

        return int(temp.strip())

    def get_net_speed(self):
        downspeed = 0.0
        upspeed = 0.0
        net = psutil.net_io_counters(pernic=True)[self.iface]        
        now = long(datetime.now().strftime('%s'))

        try:
            if self.lasttimestamp is not None:
                downspeed = (net.bytes_recv - self.lastrecv) / (now - self.lasttimestamp)
                upspeed = (net.bytes_sent - self.lastsent) / (now - self.lasttimestamp)

            if downspeed < 1024:
                down_unit = 'B'
            elif downspeed < 1048576:
                down_unit = 'KB'
                downspeed = downspeed / 1024.0
            elif downspeed < 1073741824:
                down_unit = 'MB'
                downspeed = downspeed / 1048576.0
            else:
                down_unit = 'GB'
                downspeed = downspeed / 1073741824.0

            if upspeed < 1024:
                up_unit = 'B'
            elif upspeed < 1048576:
                up_unit = 'KB'
                upspeed = upspeed / 1024.0
            elif upspeed < 1073741824:
                up_unit = 'MB'
                upspeed = upspeed / 1048576.0
            else:
                up_unit = 'GB'
                upspeed = upspeed / 1073741824.0

            self.lastrecv = net.bytes_recv
            self.lastsent = net.bytes_sent
            self.lasttimestamp = now
        except:
            downspeed = 0.0
            upspeed = 0.0
            down_unit = ""
            up_unit = ""

        return (downspeed, down_unit, upspeed, up_unit)


        uptime = res.group('uptime')
        load = res.group('load').replace(',', '')

        return (uptime, load)

    def get_gpu_temp(self):
        res = subprocess.check_output(['nvidia-settings', '-q', 'gpucoretemp'])
        temp = res.split('\n')[1].split(': ')[1].replace('.', '')

        return int(temp.strip())

    def get_batt_status(self):
        #str_battery = "Battery 0: Discharging, 5%, 5 remaining"
        str_battery=subprocess.check_output(['acpi', '-b'])
        ret = ""
        if str_battery != "":
            str_battery = str_battery.split(',')
            tmp = str_battery[1].rstrip()
            tmp = tmp[:tmp.find('%')]
            battery = int(tmp)
            if len(str_battery) > 2:
                str_battery = str_battery[2].split(' ')
            else:
                str_battery[1] = ""
            if battery > 15:
                ret += icon("bat_full_01", fg=COLOR['BLUE'])
                ret += progress(int(battery), fg=COLOR['BLUE'])
            elif battery > 8:
                ret += icon("bat_low_01", fg=COLOR['YELLOW'])
                ret += progress(int(battery), fg=COLOR['YELLOW'])
            else:
                if self.blink_batt:
                    ret += icon("bat_empty_01", fg=COLOR['RED'])
                else:
                    ret += '   '
                self.blink_batt = not self.blink_batt    
                ret += progress(int(battery), fg=COLOR['RED'])
 
            if self.refresh_batt_left_in == 0:
                self.time_batt_remaining = str_battery[1]
            ret += self.time_batt_remaining
            self.refresh_batt_left_in = (self.refresh_batt_left_in + 1) % 10
            
        return ret


if __name__=="__main__":
    PATH = os.path.abspath(os.path.dirname(__file__) + "/../")
    sys.path.append(PATH)

    from config import *

    dock = SysInfoDock()
    dock.run()
