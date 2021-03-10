import unittest.mock

from homework.hw2.task1.curry import *
from tests.utils import extract_message_string_from_context


class CurryTestCase(unittest.TestCase):
    def test_should_raise_error_when_negative_arity_is_passed_to_curry(self):
        with self.assertRaises(ValueError) as context:
            curry_explicit(lambda x: print(x), -1)

        self.assertTrue(NEGATIVE_ARITY_ERROR_MESSAGE in extract_message_string_from_context(context))

    def test_should_raise_error_when_function_has_more_arguments_than_passed_arity(self):
        with self.assertRaises(ValueError) as context:
            curry_explicit(lambda x, y: x + y, 1)

        self.assertTrue(SMALLER_ARITY_ERROR_MESSAGE in extract_message_string_from_context(context))

    def test_should_raise_error_when_function_has_less_arguments_than_passed_arity(self):
        with self.assertRaises(ValueError) as context:
            curry_explicit(lambda x, y: x + y, 3)

        self.assertTrue(BIGGER_ARITY_ERROR_MESSAGE in extract_message_string_from_context(context))

    def test_should_raise_error_when_function_positional_arguments_number_is_bigger_than_arity(self):
        with self.assertRaises(ValueError) as context:
            curry_explicit(lambda x, y, *args: print(f"{x} {y} {args}"), 1)

        self.assertTrue(
            POSITIONAL_ARGS_ARITY_INCOMPATIBILITY_ERROR_MESSAGE in extract_message_string_from_context(context)
        )

    def test_should_raise_error_when_function_with_0_arguments_take_some(self):
        with self.assertRaises(ValueError) as context:
            curried_f = curry_explicit(lambda: print("Hello world!"), 0)
            curried_f(1)

        self.assertTrue(ZERO_ARITY_ARGS_ERROR_MESSAGE in extract_message_string_from_context(context))

    def test_should_raise_error_when_calling_curried_function_with_more_than_one_argument(self):
        with self.assertRaises(ValueError) as context:
            curried_function = curry_explicit(lambda x, y: x + y, 2)
            curried_function(1, 2)

        self.assertTrue(FUNC_MULTIPLE_ARGS_ERROR_MESSAGE in extract_message_string_from_context(context))

    def test_should_curry_and_uncurry_example_functions(self):
        f2 = curry_explicit((lambda x, y: x + y), 2)
        g2 = uncurry_explicit(f2, 2)
        self.assertEqual(579, f2(123)(456))
        self.assertEqual(579, g2(123, 456))

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

    def test_should_curry_built_in_function(self):
        curried_f = curry_explicit(sum, 1)
        self.assertEqual(6, curried_f([1, 2, 3]))

    def test_should_curry_function_with_0_arguments(self):
        def f():
            return 1

        curried_f = curry_explicit(f, 0)
        self.assertEqual(1, curried_f())

    def test_should_curry_function_with_args(self):
        def f(arg1: int, arg2: int, *args):
            return sum([arg1, arg2, *args])

        curried_f = curry_explicit(f, 5)
        self.assertEqual(15, curried_f(1)(2)(3)(4)(5))

    def test_should_curry_function_with_bad_named_args(self):
        def f(arg1: int, arg2: int, *arrrrgs):
            return sum([arg1, arg2, *arrrrgs])

        curried_f = curry_explicit(f, 5)
        self.assertEqual(15, curried_f(1)(2)(3)(4)(5))
