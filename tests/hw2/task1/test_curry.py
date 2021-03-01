import io
import unittest.mock

from homwork.hw2.task1.curry import curry_explicit, uncurry_explicit


class CurryTestCase(unittest.TestCase):
    def test_should_curry_simple_function(self):
        def f(arg1: int):
            return arg1

        curried_f = curry_explicit(f, 1)
        self.assertEqual(1, curried_f(1))

    def test_should_curry_function_with_2_arguments(self):
        def f(arg1: int, arg2: int):
            return arg1 + arg2

        curried_f = curry_explicit(f, 2)
        self.assertEqual(10, curried_f(3)(7))

    def should_curry_function_with_0_arguments(self):
        def f():
            return 1

        curried_f = curry_explicit(f, 0)
        self.assertEqual(1, curried_f())
