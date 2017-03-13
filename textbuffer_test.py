# coding=utf-8

import unittest

from conf import *
from textbuffer import TextBuffer, DeleteType


class TextBufferTestCase(unittest.TestCase):
    def setUp(self):
        self.tb = TextBuffer()


class InsertTestCases(TextBufferTestCase):
    def test_insert_on_empty(self):
        self.tb.insert("Hello")
        self.assertEqual(self.tb.buffer, [['H', 'e', 'l', 'l', 'o']])
        self.assertEqual(self.tb.cursor_pos, [0, 5])
        self.assertEqual(self.tb.cursor_col, 5)

    def test_insert_at_beginning(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 0]
        self.tb.cursor_col = 0
        self.tb.insert("T")
        self.assertEqual(self.tb.buffer, [['T', 'H', 'e', 'l', 'l', 'o']])
        self.assertEqual(self.tb.cursor_pos, [0, 1])
        self.assertEqual(self.tb.cursor_col, 1)

    def test_insert_in_middle(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2]
        self.tb.cursor_col = 2
        self.tb.insert("T")
        self.assertEqual(self.tb.buffer, [['H', 'e', 'T', 'l', 'l', 'o']])
        self.assertEqual(self.tb.cursor_pos, [0, 3])
        self.assertEqual(self.tb.cursor_col, 3)

    def test_insert_at_end(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 5]
        self.tb.cursor_col = 5
        self.tb.insert("T")
        self.assertEqual(self.tb.buffer, [['H', 'e', 'l', 'l', 'o', 'T']])
        self.assertEqual(self.tb.cursor_pos, [0, 6])
        self.assertEqual(self.tb.cursor_col, 6)


class DeleteTestCases(TextBufferTestCase):
    def test_delete_on_empty(self):
        self.tb.delete()
        self.assertEqual(self.tb.buffer, [[]])
        self.assertEqual(self.tb.cursor_pos, [0, 0])
        self.assertEqual(self.tb.cursor_col, 0)

    def test_delete_in_middle(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2]
        self.tb.cursor_col = 2
        self.tb.delete()
        self.assertEqual(self.tb.buffer, [['H', 'l', 'l', 'o']])
        self.assertEqual(self.tb.cursor_pos, [0, 1])
        self.assertEqual(self.tb.cursor_col, 1)

    def test_delete_line(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o'], ['W', 'o', 'r', 'l', 'd']]
        self.tb.cursor_pos = [1, 0]
        self.tb.cursor_col = 0
        self.tb.delete()
        self.assertEqual(self.tb.buffer, [['H', 'e', 'l', 'l', 'o', 'W', 'o', 'r', 'l', 'd']])
        self.assertEqual(self.tb.cursor_pos, [0, 5])
        self.assertEqual(self.tb.cursor_col, 5)

    def test_delete_forward_on_empty(self):
        self.tb.delete(dt=DeleteType.FORWARD)
        self.assertEqual(self.tb.buffer, [[]])
        self.assertEqual(self.tb.cursor_pos, [0, 0])
        self.assertEqual(self.tb.cursor_col, 0)

    def test_delete_forward_in_middle(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2]
        self.tb.cursor_col = 2
        self.tb.delete(dt=DeleteType.FORWARD)
        self.assertEqual(self.tb.buffer, [['H', 'e', 'l', 'o']])
        self.assertEqual(self.tb.cursor_pos, [0, 2])
        self.assertEqual(self.tb.cursor_col, 2)

    def test_delete_forward_at_end(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o'], ['W', 'o', 'r', 'l', 'd']]
        self.tb.cursor_pos = [0, 5]
        self.tb.cursor_col = 5
        self.tb.delete(dt=DeleteType.FORWARD)
        self.assertEqual(self.tb.buffer, [['H', 'e', 'l', 'l', 'o', 'W', 'o', 'r', 'l', 'd']])
        self.assertEqual(self.tb.cursor_pos, [0, 5])
        self.assertEqual(self.tb.cursor_col, 5)

    def test_delete_tab(self):
        self.tb.buffer = [['H', 'e'] + list("\t" * TAB_SIZE) + ['l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2 + TAB_SIZE]
        self.tb.cursor_col = 2 + TAB_SIZE
        self.tb.delete()
        self.assertEqual(self.tb.buffer, [['H', 'e', 'l', 'l', 'o']])
        self.assertEqual(self.tb.cursor_pos, [0, 2])
        self.assertEqual(self.tb.cursor_col, 2)

    def test_delete_forward_tab(self):
        self.tb.buffer = [['H', 'e'] + list("\t" * TAB_SIZE) + ['l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2]
        self.tb.cursor_col = 2
        self.tb.delete(dt=DeleteType.FORWARD)
        self.assertEqual(self.tb.buffer, [['H', 'e', 'l', 'l', 'o']])
        self.assertEqual(self.tb.cursor_pos, [0, 2])
        self.assertEqual(self.tb.cursor_col, 2)


class CursorMovementTestCases(TextBufferTestCase):
    def test_cursor_left_on_empty(self):
        self.tb.cursor_left()
        self.assertEqual(self.tb.cursor_pos, [0, 0])
        self.assertEqual(self.tb.cursor_col, 0)

    def test_cursor_left_in_middle(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2]
        self.tb.cursor_col = 2
        self.tb.cursor_left()
        self.assertEqual(self.tb.cursor_pos, [0, 1])
        self.assertEqual(self.tb.cursor_col, 1)

    def test_cursor_left_to_end(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 1]
        self.tb.cursor_col = 1
        self.tb.cursor_left()
        self.tb.cursor_left()
        self.assertEqual(self.tb.cursor_pos, [0, 0])
        self.assertEqual(self.tb.cursor_col, 0)

    def test_cursor_left_to_prev_line(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o'], ['W', 'o', 'r', 'l', 'd']]
        self.tb.cursor_pos = [1, 0]
        self.tb.cursor_col = 0
        self.tb.cursor_left()
        self.assertEqual(self.tb.cursor_pos, [0, 5])
        self.assertEqual(self.tb.cursor_col, 5)

    def test_cursor_left_with_tab(self):
        self.tb.buffer = [['H', 'e'] + list("\t" * TAB_SIZE) + ['l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2 + TAB_SIZE]
        self.tb.cursor_col = 2 + TAB_SIZE
        self.tb.cursor_left()
        self.assertEqual(self.tb.cursor_pos, [0, 2])
        self.assertEqual(self.tb.cursor_col, 2)

    def test_cursor_right_on_empty(self):
        self.tb.cursor_right()
        self.assertEqual(self.tb.cursor_pos, [0, 0])
        self.assertEqual(self.tb.cursor_col, 0)

    def test_cursor_right_in_middle(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2]
        self.tb.cursor_col = 2
        self.tb.cursor_right()
        self.assertEqual(self.tb.cursor_pos, [0, 3])
        self.assertEqual(self.tb.cursor_col, 3)

    def test_cursor_right_to_end(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 4]
        self.tb.cursor_col = 4
        self.tb.cursor_right()
        self.tb.cursor_right()
        self.assertEqual(self.tb.cursor_pos, [0, 5])
        self.assertEqual(self.tb.cursor_col, 5)

    def test_cursor_right_to_next_line(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o'], ['W', 'o', 'r', 'l', 'd']]
        self.tb.cursor_pos = [0, 5]
        self.tb.cursor_col = 5
        self.tb.cursor_right()
        self.assertEqual(self.tb.cursor_pos, [1, 0])
        self.assertEqual(self.tb.cursor_col, 0)

    def test_cursor_right_with_tab(self):
        self.tb.buffer = [['H', 'e'] + list("\t" * TAB_SIZE) + ['l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2]
        self.tb.cursor_col = 2
        self.tb.cursor_right()
        self.assertEqual(self.tb.cursor_pos, [0, 2 + TAB_SIZE])
        self.assertEqual(self.tb.cursor_col, 2 + TAB_SIZE)

    def test_cursor_down_on_empty(self):
        self.tb.cursor_down()
        self.assertEqual(self.tb.cursor_pos, [0, 0])
        self.assertEqual(self.tb.cursor_col, 0)

    def test_cursor_down_in_middle(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o'], ['W', 'o', 'r', 'l', 'd']]
        self.tb.cursor_pos = [0, 2]
        self.tb.cursor_col = 2
        self.tb.cursor_down()
        self.assertEqual(self.tb.cursor_pos, [1, 2])
        self.assertEqual(self.tb.cursor_col, 2)

    def test_cursor_down_to_smaller_line(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o'], ['W', 'o', 'r']]
        self.tb.cursor_pos = [0, 5]
        self.tb.cursor_col = 5
        self.tb.cursor_down()
        self.assertEqual(self.tb.cursor_pos, [1, 3])
        self.assertEqual(self.tb.cursor_col, 5)

    def test_cursor_down_to_smaller_then_to_bigger_line(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o'], ['W', 'o', 'r'], ['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 5]
        self.tb.cursor_col = 5
        self.tb.cursor_down()
        self.tb.cursor_down()
        self.assertEqual(self.tb.cursor_pos, [2, 5])
        self.assertEqual(self.tb.cursor_col, 5)

    def test_cursor_down_in_middle_of_tab(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o', 'W', 'o', 'r', 'l'], ['W'] + list("\t" * TAB_SIZE) + ['o', 'r']]
        self.tb.cursor_pos = [0, 2]
        self.tb.cursor_col = 2
        self.tb.cursor_down()
        self.assertEqual(self.tb.cursor_pos, [1, 1])
        self.assertEqual(self.tb.cursor_col, 2)

        self.tb.buffer = [['H', 'e', 'l', 'l', 'o', 'W', 'o', 'r', 'l'], ['W'] + list("\t" * TAB_SIZE) + ['o', 'r']]
        self.tb.cursor_pos = [0, 1 + TAB_SIZE - 1]
        self.tb.cursor_col = 1 + TAB_SIZE - 1
        self.tb.cursor_down()
        self.assertEqual(self.tb.cursor_pos, [1, 1 + TAB_SIZE])
        self.assertEqual(self.tb.cursor_col, 1 + TAB_SIZE - 1)

    def test_cursor_up_on_empty(self):
        self.tb.cursor_up()
        self.assertEqual(self.tb.cursor_pos, [0, 0])
        self.assertEqual(self.tb.cursor_col, 0)

    def test_cursor_up_in_middle(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o'], ['W', 'o', 'r', 'l', 'd']]
        self.tb.cursor_pos = [1, 2]
        self.tb.cursor_col = 2
        self.tb.cursor_up()
        self.assertEqual(self.tb.cursor_pos, [0, 2])
        self.assertEqual(self.tb.cursor_col, 2)

    def test_cursor_up_to_smaller_line(self):
        self.tb.buffer = [['W', 'o', 'r'], ['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [1, 5]
        self.tb.cursor_col = 5
        self.tb.cursor_up()
        self.assertEqual(self.tb.cursor_pos, [0, 3])
        self.assertEqual(self.tb.cursor_col, 5)

    def test_cursor_up_to_smaller_then_bigger_line(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o'], ['W', 'o', 'r'], ['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [2, 5]
        self.tb.cursor_col = 5
        self.tb.cursor_up()
        self.tb.cursor_up()
        self.assertEqual(self.tb.cursor_pos, [0, 5])
        self.assertEqual(self.tb.cursor_col, 5)

    def test_cursor_up_in_middle_of_tab(self):
        self.tb.buffer = [['W'] + list("\t" * TAB_SIZE) + ['o', 'r'], ['H', 'e', 'l', 'l', 'o', 'W', 'o', 'r', 'l']]
        self.tb.cursor_pos = [1, 2]
        self.tb.cursor_col = 2
        self.tb.cursor_up()
        self.assertEqual(self.tb.cursor_pos, [0, 1])
        self.assertEqual(self.tb.cursor_col, 2)

        self.tb.buffer = [['W'] + list("\t" * TAB_SIZE) + ['o', 'r'], ['H', 'e', 'l', 'l', 'o', 'W', 'o', 'r', 'l']]
        self.tb.cursor_pos = [1, 1 + TAB_SIZE - 1]
        self.tb.cursor_col = 1 + TAB_SIZE - 1
        self.tb.cursor_up()
        self.assertEqual(self.tb.cursor_pos, [0, 1 + TAB_SIZE])
        self.assertEqual(self.tb.cursor_col, 1 + TAB_SIZE - 1)

    def test_cursor_to_line_begin_on_empty(self):
        self.tb.cursor_to_line_begin()
        self.assertEqual(self.tb.cursor_pos, [0, 0])
        self.assertEqual(self.tb.cursor_col, 0)

    def test_cursor_to_line_begin_in_middle(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2]
        self.tb.cursor_col = 2
        self.tb.cursor_to_line_begin()
        self.assertEqual(self.tb.cursor_pos, [0, 0])
        self.assertEqual(self.tb.cursor_col, 0)

    def test_cursor_to_line_end_on_empty(self):
        self.tb.cursor_to_line_end()
        self.assertEqual(self.tb.cursor_pos, [0, 0])
        self.assertEqual(self.tb.cursor_col, 0)

    def test_cursor_to_line_end_in_middle(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2]
        self.tb.cursor_col = 2
        self.tb.cursor_to_line_end()
        self.assertEqual(self.tb.cursor_pos, [0, 5])
        self.assertEqual(self.tb.cursor_col, 5)


class NewlineTestCases(TextBufferTestCase):
    def test_newline_on_empty(self):
        self.tb.newline()
        self.assertEqual(self.tb.buffer, [[], []])
        self.assertEqual(self.tb.cursor_pos, [1, 0])
        self.assertEqual(self.tb.cursor_col, 0)

    def test_newline_at_beginning(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.newline()
        self.assertEqual(self.tb.buffer, [[], ['H', 'e', 'l', 'l', 'o']])
        self.assertEqual(self.tb.cursor_pos, [1, 0])
        self.assertEqual(self.tb.cursor_col, 0)

    def test_newline_in_middle(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2]
        self.tb.cursor_col = 2
        self.tb.newline()
        self.assertEqual(self.tb.buffer, [['H', 'e'], ['l', 'l', 'o']])
        self.assertEqual(self.tb.cursor_pos, [1, 0])
        self.assertEqual(self.tb.cursor_col, 0)

    def test_newline_at_end(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 5]
        self.tb.cursor_col = 5
        self.tb.newline()
        self.assertEqual(self.tb.buffer, [['H', 'e', 'l', 'l', 'o'], []])
        self.assertEqual(self.tb.cursor_pos, [1, 0])
        self.assertEqual(self.tb.cursor_col, 0)


class ChangedTestCases(TextBufferTestCase):
    def test_changed_on_start(self):
        self.assertFalse(self.tb.changed)

    def test_changed_on_insert(self):
        self.tb.insert("Hello")
        self.assertTrue(self.tb.changed)

    def test_changed_on_delete(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2]
        self.tb.cursor_col = 2
        self.tb.delete()
        self.assertTrue(self.tb.changed)

    def test_changed_on_forward_delete(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2]
        self.tb.cursor_col = 2
        self.tb.delete(dt=DeleteType.FORWARD)
        self.assertTrue(self.tb.changed)

    def test_changed_on_newline(self):
        self.tb.newline()
        self.assertTrue(self.tb.changed)

    def test_changed_on_cursor_left(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2]
        self.tb.cursor_col = 2
        self.tb.cursor_left()
        self.assertFalse(self.tb.changed)

    def test_changed_on_cursor_right(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2]
        self.tb.cursor_col = 2
        self.tb.cursor_right()
        self.assertFalse(self.tb.changed)

    def test_changed_on_cursor_down(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o'], ['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2]
        self.tb.cursor_col = 2
        self.tb.cursor_down()
        self.assertFalse(self.tb.changed)

    def test_changed_on_cursor_up(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o'], ['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [1, 2]
        self.tb.cursor_col = 2
        self.tb.cursor_up()
        self.assertFalse(self.tb.changed)

    def test_changed_on_cursor_to_line_begin(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2]
        self.tb.cursor_col = 2
        self.tb.cursor_to_line_begin()
        self.assertFalse(self.tb.changed)

    def test_changed_on_cursor_to_line_end(self):
        self.tb.buffer = [['H', 'e', 'l', 'l', 'o']]
        self.tb.cursor_pos = [0, 2]
        self.tb.cursor_col = 2
        self.tb.cursor_to_line_end()
        self.assertFalse(self.tb.changed)

if __name__ == "__main__":
    unittest.main()
