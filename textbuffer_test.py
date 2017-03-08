# coding=utf-8

import unittest

from textbuffer import TextBuffer, DeleteType


class TextBufferTestCase(unittest.TestCase):
    def setUp(self):
        self.tb = TextBuffer()


class InsertTestCases(TextBufferTestCase):
    def test_insert_on_empty(self):
        self.tb.insert("Hello")
        self.assertEqual(self.tb.buffer, [['H', 'e', 'l', 'l', 'o']])
        self.assertEqual(self.tb.cursor_pos, [0, 5])

    def test_insert_at_beginning(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 0]
        self.tb.insert("T")
        self.assertEqual(self.tb.buffer, [['T', 'H', 'e', 'l', 'l', 'o']])
        self.assertEqual(self.tb.cursor_pos, [0, 1])

    def test_insert_in_middle(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2]
        self.tb.insert("T")
        self.assertEqual(self.tb.buffer, [['H', 'e', 'T', 'l', 'l', 'o']])
        self.assertEqual(self.tb.cursor_pos, [0, 3])

    def test_insert_at_end(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 5]
        self.tb.insert("T")
        self.assertEqual(self.tb.buffer, [['H', 'e', 'l', 'l', 'o', 'T']])
        self.assertEqual(self.tb.cursor_pos, [0, 6])


class DeleteTestCases(TextBufferTestCase):
    def test_delete_on_empty(self):
        self.tb.delete()
        self.assertEqual(self.tb.buffer, [[]])
        self.assertEqual(self.tb.cursor_pos, [0, 0])

    def test_delete_in_middle(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2]
        self.tb.delete()
        self.assertEqual(self.tb.buffer, [['H', 'l', 'l', 'o']])
        self.assertEqual(self.tb.cursor_pos, [0, 1])

    def test_delete_line(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o'], ['W', 'o', 'r', 'l', 'd']]
        self.tb.cursor_pos = [1, 0]
        self.tb.delete()
        self.assertEqual(self.tb.buffer, [['H', 'e', 'l', 'l', 'o', 'W', 'o', 'r', 'l', 'd']])
        self.assertEqual(self.tb.cursor_pos, [0, 5])

    def test_delete_forward_on_empty(self):
        self.tb.delete(dt=DeleteType.FORWARD)
        self.assertEqual(self.tb.buffer, [[]])
        self.assertEqual(self.tb.cursor_pos, [0, 0])

    def test_delete_forward_in_middle(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2]
        self.tb.delete(dt=DeleteType.FORWARD)
        self.assertEqual(self.tb.buffer, [['H', 'e', 'l', 'o']])
        self.assertEqual(self.tb.cursor_pos, [0, 2])

    def test_delete_forward_at_end(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o'], ['W', 'o', 'r', 'l', 'd']]
        self.tb.cursor_pos = [0, 5]
        self.tb.delete(dt=DeleteType.FORWARD)
        self.assertEqual(self.tb.buffer, [['H', 'e', 'l', 'l', 'o', 'W', 'o', 'r', 'l', 'd']])
        self.assertEqual(self.tb.cursor_pos, [0, 5])


class CursorMovementTestCases(TextBufferTestCase):
    def test_cursor_left_on_empty(self):
        self.tb.cursor_left()
        self.assertEqual(self.tb.cursor_pos, [0, 0])

    def test_cursor_left_in_middle(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2]
        self.tb.cursor_left()
        self.assertEqual(self.tb.cursor_pos, [0, 1])

    def test_cursor_left_to_end(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 1]
        self.tb.cursor_left()
        self.tb.cursor_left()
        self.assertEqual(self.tb.cursor_pos, [0, 0])

    def test_cursor_left_to_prev_line(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o'], ['W', 'o', 'r', 'l', 'd']]
        self.tb.cursor_pos = [1, 0]
        self.tb.cursor_left()
        self.assertEqual(self.tb.cursor_pos, [0, 5])

    def test_cursor_right_on_empty(self):
        self.tb.cursor_right()
        self.assertEqual(self.tb.cursor_pos, [0, 0])

    def test_cursor_right_in_middle(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2]
        self.tb.cursor_right()
        self.assertEqual(self.tb.cursor_pos, [0, 3])

    def test_cursor_right_to_end(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 4]
        self.tb.cursor_right()
        self.tb.cursor_right()
        self.assertEqual(self.tb.cursor_pos, [0, 5])

    def test_cursor_right_to_next_line(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o'], ['W', 'o', 'r', 'l', 'd']]
        self.tb.cursor_pos = [0, 5]
        self.tb.cursor_right()
        self.assertEqual(self.tb.cursor_pos, [1, 0])

    def test_cursor_down_on_empty(self):
        self.tb.cursor_down()
        self.assertEqual(self.tb.cursor_pos, [0, 0])

    def test_cursor_down_in_middle(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o'], ['W', 'o', 'r', 'l', 'd']]
        self.tb.cursor_pos = [0, 2]
        self.tb.cursor_down()
        self.assertEqual(self.tb.cursor_pos, [1, 2])

    def test_cursor_down_to_smaller_line(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o'], ['W', 'o', 'r']]
        self.tb.cursor_pos = [0, 5]
        self.tb.cursor_down()
        self.assertEqual(self.tb.cursor_pos, [1, 3])

    def test_cursor_up_on_empty(self):
        self.tb.cursor_up()
        self.assertEqual(self.tb.cursor_pos, [0, 0])

    def test_cursor_up_in_middle(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o'], ['W', 'o', 'r', 'l', 'd']]
        self.tb.cursor_pos = [1, 2]
        self.tb.cursor_up()
        self.assertEqual(self.tb.cursor_pos, [0, 2])

    def test_cursor_up_to_smaller_line(self):
        self.tb.buffer = [['W', 'o', 'r'], ['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [1, 5]
        self.tb.cursor_up()
        self.assertEqual(self.tb.cursor_pos, [0, 3])

    def test_cursor_to_line_begin_on_empty(self):
        self.tb.cursor_to_line_begin()
        self.assertEqual(self.tb.cursor_pos, [0, 0])

    def test_cursor_to_line_begin_in_middle(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2]
        self.tb.cursor_to_line_begin()
        self.assertEqual(self.tb.cursor_pos, [0, 0])

    def test_cursor_to_line_end_on_empty(self):
        self.tb.cursor_to_line_end()
        self.assertEqual(self.tb.cursor_pos, [0, 0])

    def test_cursor_to_line_end_in_middle(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2]
        self.tb.cursor_to_line_end()
        self.assertEqual(self.tb.cursor_pos, [0, 5])


class NewlineTestCases(TextBufferTestCase):
    def test_newline_on_empty(self):
        self.tb.newline()
        self.assertEqual(self.tb.buffer, [[], []])
        self.assertEqual(self.tb.cursor_pos, [1, 0])

    def test_newline_at_beginning(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.newline()
        self.assertEqual(self.tb.buffer, [[], ['H', 'e', 'l', 'l', 'o']])
        self.assertEqual(self.tb.cursor_pos, [1, 0])

    def test_newline_in_middle(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2]
        self.tb.newline()
        self.assertEqual(self.tb.buffer, [['H', 'e'], ['l', 'l', 'o']])
        self.assertEqual(self.tb.cursor_pos, [1, 0])

    def test_newline_at_end(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 5]
        self.tb.newline()
        self.assertEqual(self.tb.buffer, [['H', 'e', 'l', 'l', 'o'], []])
        self.assertEqual(self.tb.cursor_pos, [1, 0])


if __name__ == "__main__":
    unittest.main()
