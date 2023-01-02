import sys
import numpy as np
from os import path
import math
from time import sleep
sys.path.append(path.join(path.dirname(__file__),'../../'))
from animate import Window, ColorPalette
sys.path.remove(path.join(path.dirname(__file__),'../../'))
del sys

# DEFINITIONS
win = Window()
colors = ColorPalette()
win.draw_circle(
  'circ',
  r = 50,
  y = -100,
  bg = colors.green
)
win.draw_rounded_rectangle(
  'rect',
  w = 300,
  h = 40,
  y = 100
)

# ANIMATION
def draw():
    win.play_animations()
    win.draw_all()

win.queue_animations = [('globals()[\'circ\'].interpolate(\'y\', -100, 100)','globals()[\'circ\'].interpolate(\'r\', 50, 100)',),('globals()[\'circ\'].reset_pos()',),('globals()[\'rect\'].reset_neg()',),('globals()[\'rect\'].interpolate(\'w\', 300, 100)',),('sleep(1)',),('globals()[\'circ\'].interpolate(\'x\', 0, 100)',),]
win.render(draw)
