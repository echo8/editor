# coding=utf-8

import sdl2.ext

from conf import *
from textbuffer import DeleteType


class TextArea:
    def __init__(self, window, font, text_buffer, window_border, line_spacing):
        self.window = window
        self.font = font
        self.text_buffer = text_buffer
        self.window_border = window_border
        self.line_spacing = line_spacing
        self.line_start = 0
        self.line_end = self.get_line_count() - 1
        self.ch_start = 0
        self.ch_end = self.get_char_count() - 1

    def get_line_count(self):
        return (self.window.size[1] - (self.window_border[0] + self.window_border[2])) / \
               (self.font.size[1] + self.line_spacing)

    def get_char_count(self):
        return (self.window.size[0] - (self.window_border[1] + self.window_border[3])) / self.font.size[0]

    def draw(self):
        cursor_line = self.text_buffer.cursor_pos[0]
        if cursor_line < self.line_start:
            diff = self.line_start - cursor_line
            self.line_start -= diff
            self.line_end -= diff
        elif cursor_line > self.line_end:
            diff = cursor_line - self.line_end
            self.line_start += diff
            self.line_end += diff

        cursor_ch = self.text_buffer.cursor_pos[1]
        if cursor_ch < self.ch_start:
            diff = self.ch_start - cursor_ch
            self.ch_start -= diff
            self.ch_end -= diff
        elif cursor_ch > self.ch_end:
            diff = cursor_ch - self.ch_end
            self.ch_start += diff
            self.ch_end += diff

        window_surface = self.window.get_surface()
        y = self.window_border[0]
        for i in range(self.line_start, min(self.line_end + 1, len(self.text_buffer.buffer))):
            line_txt = "".join(self.text_buffer.buffer[i]).replace("\t", " ")
            self.font.render_on(window_surface,
                                line_txt[self.ch_start:min(self.ch_end + 1, len(self.text_buffer.buffer[i]))],
                                offset=(self.window_border[3], y))
            y += (self.font.size[1] + self.line_spacing)

        cursor_x1 = ((self.text_buffer.cursor_pos[1] - self.ch_start) * self.font.size[0]) + self.window_border[3]
        cursor_y1 = (self.text_buffer.cursor_pos[0] - self.line_start) * (self.font.size[1] + self.line_spacing) + \
            self.window_border[0]
        cursor_x2 = cursor_x1
        cursor_y2 = cursor_y1 + self.font.size[1]
        sdl2.ext.line(window_surface, TEXT_AREA_CURSOR_COLOR, (cursor_x1, cursor_y1, cursor_x2, cursor_y2))

    def handle_input(self, events):
        for event in events:
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_RETURN:
                    self.text_buffer.newline()
                elif event.key.keysym.sym == sdl2.SDLK_BACKSPACE:
                    self.text_buffer.delete()
                elif event.key.keysym.sym == sdl2.SDLK_DELETE:
                    self.text_buffer.delete(dt=DeleteType.FORWARD)
                elif event.key.keysym.sym == sdl2.SDLK_UP:
                    self.text_buffer.cursor_up()
                elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                    self.text_buffer.cursor_down()
                elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    self.text_buffer.cursor_right()
                elif event.key.keysym.sym == sdl2.SDLK_LEFT:
                    self.text_buffer.cursor_left()
                elif event.key.keysym.sym == sdl2.SDLK_HOME:
                    self.text_buffer.cursor_to_line_begin()
                elif event.key.keysym.sym == sdl2.SDLK_END:
                    self.text_buffer.cursor_to_line_end()
                elif event.key.keysym.sym == sdl2.SDLK_TAB:
                    self.text_buffer.insert("\t" * TAB_SIZE)
            elif event.type == sdl2.SDL_TEXTINPUT:
                self.text_buffer.insert(event.text.text)
