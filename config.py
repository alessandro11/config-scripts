import os
from subprocess import check_output


PATH = os.path.abspath(os.path.dirname(__file__))

HEIGHT = 16

COLOR = { "BG": "#050505",
          "FG": "#cccccc",
          "GREY": "#6f757b",
          "GREY2": "#2f353b",
          "BLACK": "#353535",
          "BLACK2": "#666666",
          "RED": "#ff0000",
          "RED2": "#9a6363",
          "GREEN": "#00FF00",
          "GREEN2": "#556b2f",
          "GREEN3": "#9acd32",
          "YELLOW": "#daa520",
          "YELLOW2": "#ffc123",
          "BLUE": "#204a87",
          "BLUE2": "#3465a4",
          "MAGENTA": "#ce5c00",
          "MAGENTA2": "#f57900",
          "CYAN": "#89b6e2",
          "CYAN2": "#46a4ff",
          "WHITE": "#dddddd",
          "WHITE2": "#ffffff" }
# WS = workspace
# SI = sysinfo
# CL = clock
DOCK_POS = { "WSw": "490",
            "SIx": "490",
            "SIw": "686",
            "CLx": "1176",
            "CLw": "190" }

#FONT = "-misc-fixed-medium-r-normal--14-130-75-75-c-70-iso8859-1" 
#FONT = "-*-montecarlo-medium-r-normal-*-11-*-*-*-*-*-*-*"
FONT = "xft:DejaVu Sans Mono:style=Normal:pixelsize=12:antialias=true:hinting=true"


def is_batt_plugged():
    return check_output(['acpi', '-b']) != ''
BATT_PLUGGED=is_batt_plugged()
if BATT_PLUGGED:
    DOCK_POS['WSw'] = "440"
    DOCK_POS['SIx'] = "440"
    DOCK_POS['SIw'] = "736"


def arrows():
    return "^fg(#a488d9)>^fg(#007b8c)>^fg(#444444)>^fg() "

def sep(fg=COLOR['BLUE']):
    return " ^fg(%s)|^fg() " % fg

def text(t, fg=None):
    if fg:
        return "^fg(%s)%s^fg()" % (fg, t)
    else:
        return "%s" % t

def title(t, fg=COLOR['GREY']):
    return "^fg(%s)%s^fg() " % (fg, t)

def progress(p, width=32, height=8, fg=COLOR['CYAN'], bg=COLOR['GREY2']):
    pixels = (width * p) / 100

    rect1 = "^r(%dx%d)" % (pixels, height)
    rect2 = "^r(%dx%d)" % ((width - pixels), height)

    return "^fg(%s)%s^fg(%s)%s^fg() " % (fg, rect1, bg, rect2)

def icon(i, fg=COLOR['CYAN']):
    iconfile = os.path.join(PATH, "icons/%s.xbm" % i)
    return "^fg(%s)^i(%s)^fg() " % (fg, iconfile)
