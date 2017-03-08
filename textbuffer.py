# coding=utf-8

from codecs import open


class DeleteType:
    BACK = 1
    FORWARD = 2


class TextBuffer:
    def __init__(self, text=None):
        self.buffer = [[] if text is None else list(text)]
        self.cursor_pos = [0, len(self.buffer[0])]
        self.changed = True

    def insert(self, text):
        for c in text:
            self.buffer[self.cursor_pos[0]].insert(self.cursor_pos[1], c)
            self.cursor_pos[1] += 1
        self.changed = True

    def delete(self, dt=DeleteType.BACK):
        if dt == DeleteType.BACK:
            if self.cursor_pos[1] > 0:
                del self.buffer[self.cursor_pos[0]][self.cursor_pos[1] - 1]
                self.cursor_pos[1] -= 1
            elif self.cursor_pos[0] > 0:
                old_pos = self.cursor_pos
                self.cursor_pos = [self.cursor_pos[0] - 1, len(self.buffer[self.cursor_pos[0] - 1])]
                self.buffer[old_pos[0] - 1] += self.buffer[old_pos[0]]
                del self.buffer[old_pos[0]]
        else:
            if self.cursor_pos[1] < len(self.buffer[self.cursor_pos[0]]):
                del self.buffer[self.cursor_pos[0]][self.cursor_pos[1]]
            elif self.cursor_pos[0] < len(self.buffer) - 1:
                self.buffer[self.cursor_pos[0]] += self.buffer[self.cursor_pos[0] + 1]
                del self.buffer[self.cursor_pos[0] + 1]
        self.changed = True

    def cursor_left(self):
        if self.cursor_pos[1] > 0:
            self.cursor_pos[1] -= 1
        elif self.cursor_pos[0] > 0:
            self.cursor_pos = [self.cursor_pos[0] - 1, len(self.buffer[self.cursor_pos[0] - 1])]

    def cursor_right(self):
        if self.cursor_pos[1] < len(self.buffer[self.cursor_pos[0]]):
            self.cursor_pos[1] += 1
        elif self.cursor_pos[0] < len(self.buffer) - 1:
            self.cursor_pos = [self.cursor_pos[0] + 1, 0]

    def cursor_down(self):
        if self.cursor_pos[0] < len(self.buffer) - 1:
            self.cursor_pos = [self.cursor_pos[0] + 1,
                               min(self.cursor_pos[1], len(self.buffer[self.cursor_pos[0] + 1]))]

    def cursor_up(self):
        if self.cursor_pos[0] > 0:
            self.cursor_pos = [self.cursor_pos[0] - 1,
                               min(self.cursor_pos[1], len(self.buffer[self.cursor_pos[0] - 1]))]

    def cursor_to_line_begin(self):
        self.cursor_pos[1] = 0

    def cursor_to_line_end(self):
        self.cursor_pos[1] = len(self.buffer[self.cursor_pos[0]])

    def newline(self):
        self.buffer.insert(self.cursor_pos[0] + 1,
                           self.buffer[self.cursor_pos[0]][self.cursor_pos[1]:len(self.buffer[self.cursor_pos[0]])])
        self.buffer[self.cursor_pos[0]] = self.buffer[self.cursor_pos[0]][:self.cursor_pos[1]]
        self.cursor_pos = [self.cursor_pos[0] + 1, 0]
        self.changed = True

    def get_value(self):
        return "".join(self.buffer[0])

    def load(self, file_path):
        with open(file_path, 'r', 'utf-8') as f:
            self.buffer = []
            self.changed = False
            for line in f:
                l = []
                for c in line.rstrip("\n\r"):
                    l.append(c)
                self.buffer.append(l)
            if self.buffer is []:
                self.buffer.append([])

    def save(self, file_path):
        with open(file_path, 'w', 'utf-8') as f:
            self.changed = False
            for line in self.buffer:
                f.write("".join(line) + '\n')
