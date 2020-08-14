# -------------------------------- IMPORT MODULES --------------------------------
from docopt import *
from colr import color
import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime as dt


# -------------------------------- COLORS --------------------------------
colors = ['#f891a0', '#c1dee7', '#cb7f07', '#6389df', '#c7bab1', '#728239', '#a6b401', '#4a9396', '#fd742d']


# -------------------------------- FUNCTIONS --------------------------------
def generateTree(path): 
    global colors
    i = 0
    text = ""

    for root, dirs, files in os.walk(path):
        root = root.replace(path, "")
        # count the seperator -> it tells the level
        level = root.count(os.sep)

        if level == 0:
            text += color(path + "\n", fore='firebrick')
            for file in files:
                text += color("  "*level + "|--", 'firebrick')
                text += color(file + "\n", colors[i])
                i += 1

        else:
            text += color("|" + "--"*level + root + "\n", fore='firebrick', style='bright')
            for file in files:
                if i == len(colors): i = 0
                text += color("|" + "  "*level + "|--", 'firebrick')
                text += color(file + "\n", colors[i])
                i += 1

        text += color("|\n", fore='firebrick')
    return text


def searchFile(dir_path, filename):
    global colors
    i = 0
    text = ""

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if filename in file:
                if i == len(colors):
                    i = 0
                text += color("\n" + os.path.join(root,file), fore=colors[i])
                i += 1
    return text

def getWidth(text):
    max_ch = 0
    no_of_char = 0
    for ch in text:
        if ch == "\n":
            if no_of_char > max_ch:
                max_ch = no_of_char
            no_of_char = 0
        else:
            no_of_char += 1
    return max_ch*8
        

def getHeight(text):
    lines = 0
    for ch in text:
        if ch == "\n":
            lines += 1
    return lines*23


def saveImageForTree(dir_path):
    global colors
    i = 0
    line = 5

    width = getWidth(generateTree(dir_path))
    height = getHeight(generateTree(dir_path))

    #print(f"{width} -> {height}")

    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('bahnschrift.ttf', 18)

    for root, dirs, files in os.walk(dir_path):
        root = root.replace(dir_path, "")
        # count the seperator -> it tells the level
        level = root.count(os.sep)

        if level == 0:
            draw.text((5,line), dir_path + "\n", fill='firebrick', font=font)
            line += 22
            for file in files:
                draw.text((5,line), "  "*level + "|--" + file + "\n", fill=colors[i], font=font)
                i += 1
                line += 22

        else:
            draw.text((5,line), "|" + "--"*level + root + "\n", fill='firebrick', font=font)
            line += 22
            for file in files:
                if i == len(colors): i = 0
                draw.text((5,line), "|" + "  "*level + "|--" + file + "\n", fill=colors[i], font=font)
                i += 1
                line += 22

        draw.text((5,line), "|\n", fill='white', font=font)
        line += 22


    filename = "DTG_CMD_" + str(dt.now().year) + str(dt.now().month) + str(dt.now().day) + "_" + str(dt.now().hour) + str(dt.now().minute) + str(dt.now().second) + str(dt.now().microsecond) + '.png'

    image.save(filename)
    print(color("Image saved successfully as " + filename + ".", fore='green'))
    image.show(command='display')


def saveImageForSearch(dir_path, filename):
    global colors
    i = 0
    line = 5

    width = getWidth(searchFile(dir_path, filename))
    height = getHeight(searchFile(dir_path, filename))

    #print(f"{width} -> {height}")

    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('bahnschrift.ttf', 18)

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if filename in file:
                if i == len(colors):
                    i = 0
                draw.text((5,line), os.path.join(root,file), fill=colors[i], font=font)
                i += 1
                line += 22

    filename = "DTG_CMD_" + str(dt.now().year) + str(dt.now().month) + str(dt.now().day) + "_" + str(dt.now().hour) + str(dt.now().minute) + str(dt.now().second) + str(dt.now().microsecond) + '.png'

    image.save(filename)
    print(color("Image saved successfully as " + filename + ".", fore='green'))
    image.show(command='display')


# -------------------------------- DOCOPT USAGE --------------------------------  

usage = ''' 

Directory Tree Generator

Usage:
    main.py tree <directory_path>
    main.py search <directory_path> <filename>
    main.py save <directory_path>
    main.py save <directory_path> <filename>

'''

# -------------------------------- MAIN --------------------------------

args = docopt(usage)

if args['tree']:
    output = generateTree(args['<directory_path>'])
    print(output)

if args['search']:
    output = searchFile(args['<directory_path>'], args['<filename>'])
    print(output)

if args['save']:

    if(args['<filename>']):
        saveImageForSearch(args['<directory_path>'], args['<filename>'])
    else:
        saveImageForTree(args['<directory_path>'])
    