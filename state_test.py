# coding=utf-8

import unittest
import sdl2.ext

from state import *


class TextBufferMock:
    def __init__(self):
        self.changed = False


class TextAreaMock:
    def __init__(self):
        self.text_buffer = TextBufferMock()

    def draw(self):
        pass

    def handle_input(self, events):
        pass


class StatusBarMock:
    def __init__(self):
        pass

    def draw(self):
        pass

    def init_input(self, label, text=None):
        pass

    def draw_label(self):
        pass

    def draw_input(self):
        pass

    def handle_input(self, events):
        pass

    def display_msg(self, msg):
        pass


class EventMock:
    def __init__(self):
        pass


def get_key_down_event(sym):
    e = EventMock()
    e.type = sdl2.SDL_KEYDOWN
    e.key = EventMock()
    e.key.keysym = EventMock()
    e.key.keysym.sym = sym
    return e


class StateTestCase(unittest.TestCase):
    def setUp(self):
        self.state = EditState(Editor(None, None, TextAreaMock(), StatusBarMock()))
        self.state.update_only = True


class EditTestCases(StateTestCase):
    def test_quit(self):
        res = self.state.update([get_key_down_event(sdl2.SDLK_LCTRL), get_key_down_event(sdl2.SDLK_q)])
        self.assertTrue(isinstance(res, QuitState))
        res = self.state.update([get_key_down_event(sdl2.SDLK_RCTRL), get_key_down_event(sdl2.SDLK_q)])
        self.assertTrue(isinstance(res, QuitState))

    def test_open(self):
        res = self.state.update([get_key_down_event(sdl2.SDLK_LCTRL), get_key_down_event(sdl2.SDLK_o)])
        self.assertTrue(isinstance(res, OpenState))
        res = self.state.update([get_key_down_event(sdl2.SDLK_RCTRL), get_key_down_event(sdl2.SDLK_o)])
        self.assertTrue(isinstance(res, OpenState))

    def test_save(self):
        res = self.state.update([get_key_down_event(sdl2.SDLK_LCTRL), get_key_down_event(sdl2.SDLK_s)])
        self.assertTrue(isinstance(res, SaveState))
        res = self.state.update([get_key_down_event(sdl2.SDLK_RCTRL), get_key_down_event(sdl2.SDLK_s)])
        self.assertTrue(isinstance(res, SaveState))

    def test_save_as(self):
        res = self.state.update([get_key_down_event(sdl2.SDLK_LCTRL), get_key_down_event(sdl2.SDLK_LSHIFT),
                                 get_key_down_event(sdl2.SDLK_s)])
        self.assertTrue(isinstance(res, SaveState))
        res = self.state.update([get_key_down_event(sdl2.SDLK_LCTRL), get_key_down_event(sdl2.SDLK_RSHIFT),
                                 get_key_down_event(sdl2.SDLK_s)])
        self.assertTrue(isinstance(res, SaveState))
        res = self.state.update([get_key_down_event(sdl2.SDLK_RCTRL), get_key_down_event(sdl2.SDLK_LSHIFT),
                                 get_key_down_event(sdl2.SDLK_s)])
        self.assertTrue(isinstance(res, SaveState))
        res = self.state.update([get_key_down_event(sdl2.SDLK_RCTRL), get_key_down_event(sdl2.SDLK_RSHIFT),
                                 get_key_down_event(sdl2.SDLK_s)])
        self.assertTrue(isinstance(res, SaveState))

    def test_quit_with_changes(self):
        self.state.editor.text_area.text_buffer.changed = True
        res = self.state.update([get_key_down_event(sdl2.SDLK_LCTRL), get_key_down_event(sdl2.SDLK_q)])
        self.assertTrue(isinstance(res, SaveChangesState))

    def test_open_with_changes(self):
        self.state.editor.text_area.text_buffer.changed = True
        res = self.state.update([get_key_down_event(sdl2.SDLK_LCTRL), get_key_down_event(sdl2.SDLK_o)])
        self.assertTrue(isinstance(res, SaveChangesState))
