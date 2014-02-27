import os

PATH = os.path.abspath(os.path.dirname(__file__))

HEIGHT = 16

COLOR = { "BG": "#050505",
          "FG": "#cccccc",
          "GREY": "#6f757b",
          "GREY2": "#2f353b",
          "BLACK": "#353535",
          "BLACK2": "#666666",
          "RED": "#ae4747",
          "RED2": "#ee6363",
          "GREEN": "#556b2f",
          "GREEN2": "#9acd32",
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

FONT = "-misc-fixed-medium-r-normal--14-130-75-75-c-70-iso8859-1" 
# "-*-montecarlo-medium-r-normal-*-11-*-*-*-*-*-*-*"

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
