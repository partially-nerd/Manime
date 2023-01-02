from re import sub, findall
from sys import argv
from os import system as cmd

template = """import sys
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
{REPLACE THIS FOR DEFINITIONS}

# ANIMATION
def draw():
    win.play_animations()
    win.draw_all()

win.queue_animations = [{REPLACE THIS FOR ANIMATIONS}]
win.render(draw)
"""

file = argv[1]
out_file = argv[2]
try: output_mp4 = "--nosave" if len(argv) < 1 else argv[3]
except: pass

with open(file, "r") as file_:
    content = file_.read()

definitions = content.split("```py\n")[1].split("\n```")[0]
animations = content.split("```lua\n")[1].split("\n```")[0]
code_block = ""

definitions = definitions.replace(":", "=")
definitions = sub("\__", "win.draw_", definitions)

for line in animations.split("\n"):
    code_block += "("
        
    if "reset_pos" in line:
        print(code_block)
        name = line.split(" : ")[0]
        code_block += f"'globals()[\\'{name}\\'].reset_pos()',"

    elif "reset_neg" in line:
        name = line.split(" : ")[0]
        code_block += f"'globals()[\\'{name}\\'].reset_neg()',"

    elif "pause" in line:
        time = line.split(" : ")[1]
        code_block += f"'sleep({time})',"

    else:
        if " + " in line:
            for animation in line.split(" + "):
                name = animation.split(" : ")[0]
                param = animation.split(" : ")[1].split(" = ")[0]
                start = animation.split(" = ")[1].split(" -> ")[0]
                end = animation.split(" -> ")[1]
                code_block += f"'globals()[\\'{name}\\'].interpolate(\\'{param}\\', {start}, {end})',"
        else:
            name = line.split(" : ")[0]
            param = line.split(" : ")[1].split(" = ")[0]
            start = line.split(" = ")[1].split(" -> ")[0]
            end = line.split(" -> ")[1]
            code_block += f"'globals()[\\'{name}\\'].interpolate(\\'{param}\\', {start}, {end})',"

    code_block += "),"

template = template.replace("{REPLACE THIS FOR DEFINITIONS}", definitions).replace("{REPLACE THIS FOR ANIMATIONS}", code_block)

with open(out_file, "w") as file_:
    file_.write(template)
