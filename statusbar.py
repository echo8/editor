# coding=utf-8

import sdl2.ext

from conf import *
from textarea import TextArea
from textbuffer import TextBuffer


class StatusBar:
    def __init__(self, window, text_buffer, font, color, border):
        self.window = window
        self.text_buffer = text_buffer
        self.font = font
        self.color = color
        self.border = border
        self.height = font.size[1] + border[0] + border[2]
        self.width = window.size[0]
        self.msg = None
        self.msg_timeout = None
        self.input = None
        self.input_label = None

    def get_line_pos_text(self):
        return "{}:{}".format(self.text_buffer.cursor_pos[0] + 1, self.text_buffer.cursor_pos[1] + 1)

    def draw(self):
        window_surface = self.window.get_surface()
        sb_y = self.window.size[1] - self.height
        sdl2.ext.fill(window_surface, self.color, area=(0, sb_y, self.width, self.height))

        text = self.get_line_pos_text()
        self.font.render_on(window_surface,
                            text,
                            offset=(self.window.size[0] - ((self.font.size[0] * len(text)) + self.border[1]),
                                    sb_y + self.border[0]))

        if self.msg_timeout is not None and sdl2.SDL_GetTicks() < self.msg_timeout:
            self.font.render_on(window_surface,
                                self.msg,
                                offset=(self.border[1], self.window.size[1] - self.height + self.border[0]))
        elif self.msg_timeout is not None:
            self.msg_timeout = None

    def init_input(self, label, text=None):
        self.input_label = label
        self.input = TextArea(self.window, self.font, TextBuffer(text),
                              window_border=(self.window.size[1] - self.height + self.border[0],
                                             self.border[1],
                                             self.border[2],
                                             (self.font.size[0] * len(label)) + (2*self.border[3])),
                              line_spacing=0)

    def draw_label(self):
        window_surface = self.window.get_surface()
        sdl2.ext.fill(window_surface, self.color,
                      area=(0, self.window.size[1] - self.height, self.width, self.height))
        self.font.render_on(window_surface,
                            self.input_label,
                            offset=(self.border[1], self.window.size[1] - self.height + self.border[0]))

    def draw_input(self):
        self.draw_label()
        self.input.draw()

    def handle_input(self, events):
        self.input.handle_input(events)

    def display_msg(self, msg, duration=STATUS_BAR_MSG_DURATION):
        self.msg = msg
        self.msg_timeout = sdl2.SDL_GetTicks() + duration
