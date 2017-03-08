# coding=utf-8

import argparse
import sys
import sdl2.ext

from conf import *
from textbuffer import TextBuffer
from textarea import TextArea
from statusbar import StatusBar
from state import Editor, EditState


def res(s):
    try:
        return map(int, s.split(','))
    except:
        raise argparse.ArgumentTypeError("Resolution must be in x,y format.")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?", help="file to edit")
    parser.add_argument("-r", "--resolution", type=res, help="size of window in x,y format")
    args = parser.parse_args()

    window_size = WINDOW_SIZE
    if args.resolution:
        window_size = args.resolution

    return window_size, args.file


def run():
    (window_size, f) = get_args()

    tb = TextBuffer()
    if f:
        tb.load(f)

    sdl2.ext.init()
    window = sdl2.ext.Window(WINDOW_TITLE, size=window_size)
    window.show()

    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)

    font_img = factory.from_image(FONT_IMG_PATH)
    sdl2.SDL_SetColorKey(font_img.surface, sdl2.SDL_TRUE,
                         sdl2.SDL_MapRGB(font_img.surface.format, COLOR_KEY_R, COLOR_KEY_G, COLOR_KEY_B))
    font = sdl2.ext.BitmapFont(font_img, FONT_SIZE, mapping=FONT_MAPPING)

    sb = StatusBar(window, tb, font, STATUS_BAR_COLOR, (STATUS_BAR_BORDER_TOP,
                                                        STATUS_BAR_BORDER_RIGHT,
                                                        STATUS_BAR_BORDER_BOTTOM,
                                                        STATUS_BAR_BORDER_LEFT))
    ta = TextArea(window, font, tb, (TEXT_AREA_BORDER_TOP,
                                     TEXT_AREA_BORDER_RIGHT,
                                     sb.height + TEXT_AREA_BORDER_BOTTOM,
                                     TEXT_AREA_BORDER_LEFT),
                  TEXT_AREA_LINE_SPACING)
    state = EditState(Editor(None, window, ta, sb))

    sdl2.SDL_StartTextInput()

    while True:
        state = state.update(sdl2.ext.get_events())
        if state is None:
            break

    sdl2.SDL_StopTextInput()
    sdl2.ext.quit()
    return 0


if __name__ == "__main__":
    sys.exit(run())
