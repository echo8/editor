# coding=utf-8

from conf import *

DELETE_BACK = 1
DELETE_FORWARD = 2


class TextBuffer:
    def __init__(self, text=None):
        self.buffer = [[] if text is None else list(text)]
        self.cursor_pos = [0, len(self.buffer[0])]
        self.cursor_col = self.cursor_pos[1]
        self.changed = False

    def insert(self, text):
        for c in text:
            self.buffer[self.cursor_pos[0]].insert(self.cursor_pos[1], c)
            self.cursor_pos[1] += 1
        self.changed = True
        self.cursor_col = self.cursor_pos[1]

    def delete(self, dt=DELETE_BACK):
        if dt == DELETE_BACK:
            if self.cursor_pos[1] > 0:
                if self.buffer[self.cursor_pos[0]][self.cursor_pos[1] - 1] != "\t":
                    del self.buffer[self.cursor_pos[0]][self.cursor_pos[1] - 1]
                    self.cursor_pos[1] -= 1
                else:
                    del self.buffer[self.cursor_pos[0]][self.cursor_pos[1] - TAB_SIZE:self.cursor_pos[1]]
                    self.cursor_pos[1] -= TAB_SIZE
            elif self.cursor_pos[0] > 0:
                old_pos = self.cursor_pos
                self.cursor_pos = [self.cursor_pos[0] - 1, len(self.buffer[self.cursor_pos[0] - 1])]
                self.buffer[old_pos[0] - 1] += self.buffer[old_pos[0]]
                del self.buffer[old_pos[0]]
        else:
            if self.cursor_pos[1] < len(self.buffer[self.cursor_pos[0]]):
                if self.buffer[self.cursor_pos[0]][self.cursor_pos[1]] != "\t":
                    del self.buffer[self.cursor_pos[0]][self.cursor_pos[1]]
                else:
                    del self.buffer[self.cursor_pos[0]][self.cursor_pos[1]:self.cursor_pos[1] + TAB_SIZE]
            elif self.cursor_pos[0] < len(self.buffer) - 1:
                self.buffer[self.cursor_pos[0]] += self.buffer[self.cursor_pos[0] + 1]
                del self.buffer[self.cursor_pos[0] + 1]
        self.changed = True
        self.cursor_col = self.cursor_pos[1]

    def cursor_left(self):
        if self.cursor_pos[1] > 0:
            if self.buffer[self.cursor_pos[0]][self.cursor_pos[1] - 1] != "\t":
                self.cursor_pos[1] -= 1
            else:
                self.cursor_pos[1] -= TAB_SIZE
        elif self.cursor_pos[0] > 0:
            self.cursor_pos = [self.cursor_pos[0] - 1, len(self.buffer[self.cursor_pos[0] - 1])]
        self.cursor_col = self.cursor_pos[1]

    def cursor_right(self):
        if self.cursor_pos[1] < len(self.buffer[self.cursor_pos[0]]):
            if self.buffer[self.cursor_pos[0]][self.cursor_pos[1]] != "\t":
                self.cursor_pos[1] += 1
            else:
                self.cursor_pos[1] += TAB_SIZE
        elif self.cursor_pos[0] < len(self.buffer) - 1:
            self.cursor_pos = [self.cursor_pos[0] + 1, 0]
        self.cursor_col = self.cursor_pos[1]

    def cursor_down(self):
        if self.cursor_pos[0] < len(self.buffer) - 1:
            self.cursor_pos = [self.cursor_pos[0] + 1,
                               min(self.cursor_col, len(self.buffer[self.cursor_pos[0] + 1]))]
            if self._middle_of_tab():
                self.cursor_pos[1] = self._closest_tab_edge()

    def cursor_up(self):
        if self.cursor_pos[0] > 0:
            self.cursor_pos = [self.cursor_pos[0] - 1,
                               min(self.cursor_col, len(self.buffer[self.cursor_pos[0] - 1]))]
            if self._middle_of_tab():
                self.cursor_pos[1] = self._closest_tab_edge()

    def _middle_of_tab(self):
        return self.cursor_pos[1] != len(self.buffer[self.cursor_pos[0]]) and \
               self.buffer[self.cursor_pos[0]][self.cursor_pos[1]] == "\t" and \
               self.cursor_pos[1] - 1 >= 0 and self.buffer[self.cursor_pos[0]][self.cursor_pos[1] - 1] == "\t"

    def _closest_tab_edge(self):
        left_edge = self.cursor_pos[1]
        while left_edge > 0 and self.buffer[self.cursor_pos[0]][left_edge - 1] == "\t":
            left_edge -= 1

        right_edge = self.cursor_pos[1]
        while right_edge < len(self.buffer[self.cursor_pos[0]]) and \
                self.buffer[self.cursor_pos[0]][left_edge + 1] == "\t":
            right_edge += 1

        if right_edge - left_edge > TAB_SIZE:
            r = (self.cursor_pos[1] - left_edge) % TAB_SIZE
            if r == 0:
                return self.cursor_pos[1]
            else:
                left_edge = self.cursor_pos[1] - r
                right_edge = self.cursor_pos[1] + (TAB_SIZE - r)

        if right_edge - self.cursor_pos[1] < self.cursor_pos[1] - left_edge:
            return right_edge
        else:
            return left_edge

    def cursor_to_line_begin(self):
        self.cursor_pos[1] = 0
        self.cursor_col = self.cursor_pos[1]

    def cursor_to_line_end(self):
        self.cursor_pos[1] = len(self.buffer[self.cursor_pos[0]])
        self.cursor_col = self.cursor_pos[1]

    def newline(self):
        self.buffer.insert(self.cursor_pos[0] + 1,
                           self.buffer[self.cursor_pos[0]][self.cursor_pos[1]:len(self.buffer[self.cursor_pos[0]])])
        self.buffer[self.cursor_pos[0]] = self.buffer[self.cursor_pos[0]][:self.cursor_pos[1]]
        self.cursor_pos = [self.cursor_pos[0] + 1, 0]
        self.changed = True
        self.cursor_col = self.cursor_pos[1]

    def get_value(self):
        return "".join(self.buffer[0])

    def clear(self):
        self.buffer = [[]]
        self.cursor_pos = [0, 0]
        self.cursor_col = self.cursor_pos[1]
        self.changed = False

    def load(self, file_path):
        with open(file_path, 'r') as f:
            self.buffer = []
            self.cursor_pos = [0, 0]
            self.cursor_col = self.cursor_pos[1]
            self.changed = False
            for line in f:
                l = []
                for c in line.replace("\t", "\t" * TAB_SIZE).rstrip("\n\r"):
                    l.append(c)
                self.buffer.append(l)
            if self.buffer is []:
                self.buffer.append([])

    def save(self, file_path):
        with open(file_path, 'w') as f:
            self.changed = False
            for i, line in enumerate(self.buffer):
                f.write("".join(line).replace("\t" * TAB_SIZE, "\t"))
                if i != len(self.buffer) - 1:
                    f.write("\n")
