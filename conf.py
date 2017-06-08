# coding=utf-8

import sdl2.ext

from inspect import getsourcefile
from os.path import abspath, dirname, join

WINDOW_TITLE = "Editor"
WINDOW_SIZE = (320, 260)

FONT_IMG_PATH = join(dirname(abspath(getsourcefile(lambda: 0))), "resources", "font.bmp")
FONT_SIZE = (7, 14)
FONT_MAPPING = [" !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdef",
                "ghijklmnopqrstuvwxyz{|}~"]

FRAMES_PER_SECOND = 30

TAB_SIZE = 4

COLOR_KEY_R = 0
COLOR_KEY_G = 0
COLOR_KEY_B = 0

BACKGROUND_COLOR = sdl2.ext.Color(0, 0, 0)

STATUS_BAR_COLOR = sdl2.ext.Color(75, 75, 75)
STATUS_BAR_BORDER_TOP = 2
STATUS_BAR_BORDER_RIGHT = 1
STATUS_BAR_BORDER_BOTTOM = 2
STATUS_BAR_BORDER_LEFT = 1
STATUS_BAR_MSG_DURATION = 2000

TEXT_AREA_BORDER_TOP = 1
TEXT_AREA_BORDER_RIGHT = 1
TEXT_AREA_BORDER_BOTTOM = 1
TEXT_AREA_BORDER_LEFT = 1
TEXT_AREA_LINE_SPACING = 1
TEXT_AREA_CURSOR_COLOR = sdl2.ext.Color(255, 255, 255)

MSG_SAVED = "Saved."
MSG_FAILED = "Failed."

INPUT_LABEL_SAVE = "Save:"
INPUT_LABEL_SAVE_CHANGES = "Save changes?"
INPUT_LABEL_OPEN = "Open:"
