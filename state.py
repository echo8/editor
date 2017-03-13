# coding=utf-8

import sdl2.ext

from conf import *


class Editor:
    def __init__(self, file_path, window, text_area, status_bar):
        self.file_path = file_path
        self.window = window
        self.text_area = text_area
        self.status_bar = status_bar


class EditorState:
    def __init__(self, editor, update_only=True):
        self.editor = editor
        self.update_only = update_only

    def changed(self):
        return self.editor.text_area.text_buffer.changed

    def update(self, events):
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                if self.changed():
                    return SaveChangesState(self.editor, QuitState)
                else:
                    return QuitState(self.editor)
        state = self.handle_input(events)
        if not self.update_only:
            sdl2.SDL_Delay(10)
            self.draw()
            self.editor.window.refresh()
        return state

    def handle_input(self, events):
        return self

    def draw(self):
        pass


class EditState(EditorState):
    def __init__(self, editor):
        EditorState.__init__(self, editor)
        self.ctrl = False
        self.shift = False
        self.o = False
        self.s = False
        self.q = False

    def handle_input(self, events):
        for event in events:
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_LCTRL or event.key.keysym.sym == sdl2.SDLK_RCTRL:
                    self.ctrl = True
                elif event.key.keysym.sym == sdl2.SDLK_LSHIFT or event.key.keysym.sym == sdl2.SDLK_RSHIFT:
                    self.shift = True
                elif event.key.keysym.sym == sdl2.SDLK_o:
                    self.o = True
                elif event.key.keysym.sym == sdl2.SDLK_s:
                    self.s = True
                elif event.key.keysym.sym == sdl2.SDLK_q:
                    self.q = True
            elif event.type == sdl2.SDL_KEYUP:
                if event.key.keysym.sym == sdl2.SDLK_LCTRL or event.key.keysym.sym == sdl2.SDLK_RCTRL:
                    self.ctrl = False
                elif event.key.keysym.sym == sdl2.SDLK_LSHIFT or event.key.keysym.sym == sdl2.SDLK_RSHIFT:
                    self.shift = False
                elif event.key.keysym.sym == sdl2.SDLK_o:
                    self.o = False
                elif event.key.keysym.sym == sdl2.SDLK_s:
                    self.s = False
                elif event.key.keysym.sym == sdl2.SDLK_q:
                    self.q = False
        if self.ctrl and self.q:
            if self.changed():
                return SaveChangesState(self.editor, QuitState)
            else:
                return QuitState(self.editor)
        elif self.ctrl and self.o:
            if self.changed():
                return SaveChangesState(self.editor, OpenState)
            else:
                return OpenState(self.editor)
        elif self.ctrl and self.s:
            if self.editor.file_path is None:
                return SaveState(self.editor)
            else:
                try:
                    self.editor.text_area.text_buffer.save(self.editor.file_path)
                    self.editor.status_bar.display_msg(MSG_SAVED)
                except IOError:
                    self.editor.status_bar.display_msg(MSG_FAILED)
        elif self.ctrl and self.shift and self.s:
            return SaveState(self.editor)
        self.editor.text_area.handle_input(events)
        return self

    def draw(self):
        sdl2.ext.fill(self.editor.window.get_surface(), BACKGROUND_COLOR)
        self.editor.text_area.draw()
        self.editor.status_bar.draw()


class SaveState(EditorState):
    def __init__(self, editor, final_state=None):
        EditorState.__init__(self, editor)
        self.editor.status_bar.init_input(INPUT_LABEL_SAVE, self.editor.file_path)
        self.final_state = final_state

    def handle_input(self, events):
        for event in events:
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    return EditState(self.editor)
                elif event.key.keysym.sym == sdl2.SDLK_RETURN:
                    old_file_path = self.editor.file_path
                    self.editor.file_path = self.editor.status_bar.input.text_buffer.get_value()
                    try:
                        self.editor.text_area.text_buffer.save(self.editor.file_path)
                    except IOError:
                        self.editor.status_bar.display_msg(MSG_FAILED)
                        self.editor.file_path = old_file_path
                        return EditState(self.editor)
                    return self.final_state(self.editor) if self.final_state is not None else EditState(self.editor)
        self.editor.status_bar.handle_input(events)
        return self

    def draw(self):
        self.editor.status_bar.draw_input()


class SaveChangesState(EditorState):
    def __init__(self, editor, final_state):
        EditorState.__init__(self, editor)
        self.editor.status_bar.init_input(INPUT_LABEL_SAVE_CHANGES, self.editor.file_path)
        self.final_state = final_state

    def handle_input(self, events):
        for event in events:
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    return EditState(self.editor)
                elif event.key.keysym.sym == sdl2.SDLK_y:
                    return SaveState(self.editor, final_state=self.final_state)
                elif event.key.keysym.sym == sdl2.SDLK_n:
                    return self.final_state(self.editor)
        return self

    def draw(self):
        self.editor.status_bar.draw_label()


class OpenState(EditorState):
    def __init__(self, editor, final_state=None):
        EditorState.__init__(self, editor)
        self.editor.status_bar.init_input(INPUT_LABEL_OPEN)
        self.final_state = final_state

    def handle_input(self, events):
        for event in events:
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    return EditState(self.editor)
                elif event.key.keysym.sym == sdl2.SDLK_RETURN:
                    old_file_path = self.editor.file_path
                    self.editor.file_path = self.editor.status_bar.input.text_buffer.get_value()
                    try:
                        self.editor.text_area.text_buffer.load(self.editor.file_path)
                    except IOError:
                        self.editor.status_bar.display_msg(MSG_FAILED)
                        self.editor.file_path = old_file_path
                        return EditState(self.editor)
                    return self.final_state(self.editor) if self.final_state is not None else EditState(self.editor)
        self.editor.status_bar.handle_input(events)
        return self

    def draw(self):
        self.editor.status_bar.draw_input()


class QuitState(EditorState):
    def __init__(self, editor):
        EditorState.__init__(self, editor)

    def update(self, events):
        return None
