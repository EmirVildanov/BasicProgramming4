import io
import unittest.mock

from homwork.hw2.task1.curry import curry_explicit, uncurry_explicit


class CurryTestCase(unittest.TestCase):
    def test_should_raise_error_when_negative_arity_is_passed_to_curry(self):
        with self.assertRaises(ValueError) as context:
            curry_explicit(lambda x: print(x), -1)

        self.assertTrue("Arity can not be negative" in str(context.exception))

    def test_should_raise_error_when_negative_arity_is_passed_to_uncurry(self):
        with self.assertRaises(ValueError) as context:
            uncurry_explicit(lambda x: print(x), -1)

        self.assertTrue("Arity can not be negative" in str(context.exception))

    def test_should_raise_error_when_function_has_more_arguments_than_passed_arity(self):
        with self.assertRaises(ValueError) as context:
            curry_explicit(lambda x, y: x+y, 1)

        self.assertTrue("Arity is smaller than fun arguments number" in str(context.exception))

    def test_should_raise_error_when_function_has_less_arguments_than_passed_arity(self):
        with self.assertRaises(ValueError) as context:
            curry_explicit(lambda x, y: x+y, 3)

        self.assertTrue("Arity is bigger than fun arguments number" in str(context.exception))

    def test_should_raise_error_when_function_positional_arguments_number_is_bigger_than_arity(self):
        with self.assertRaises(ValueError) as context:
            curry_explicit(lambda x, y, *args: print(f"{x} {y} {args}"), 1)

        print(context.exception)
        self.assertTrue("Arity is smaller than positional functions arguments number" in str(context.exception))

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

    def should_uncurry_function_with_0_arguments(self):
        def f():
            return 1

        curried_f = curry_explicit(f, 0)
        uncurried_f = uncurry_explicit(curried_f, 0)
        self.assertEqual(1, uncurried_f())
