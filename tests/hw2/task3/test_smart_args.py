import random
import unittest

from homework.hw2.task3.smart_args import smart_args, Isolated, Evaluated


@smart_args
def do_operation_over_list(*, test_list=Isolated()):
    test_list[0] = -1


@smart_args
def do_operation_over_dict(*, test_dict=Isolated()):
    test_dict["a"] = 1


class SmartArgsTestCase(unittest.TestCase):
    def test_should_isolate_passed_list_argument(self):
        initial_list = [1]
        do_operation_over_list(test_list=initial_list)
        self.assertEqual(1, initial_list[0])

    def test_should_isolate_passed_dict_argument(self):
        initial_dict = {"a": 10}
        do_operation_over_dict(test_dict=initial_dict)
        self.assertEqual(10, initial_dict["a"])
