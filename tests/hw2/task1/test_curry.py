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
            curry_explicit(lambda x, y: x + y, 1)

        self.assertTrue("Arity is smaller than fun arguments number" in str(context.exception))

    def test_should_raise_error_when_function_has_less_arguments_than_passed_arity(self):
        with self.assertRaises(ValueError) as context:
            curry_explicit(lambda x, y: x + y, 3)

        self.assertTrue("Arity is bigger than fun arguments number" in str(context.exception))

    def test_should_raise_error_when_function_positional_arguments_number_is_bigger_than_arity(self):
        with self.assertRaises(ValueError) as context:
            curry_explicit(lambda x, y, *args: print(f"{x} {y} {args}"), 1)

        self.assertTrue("Arity is smaller than positional functions arguments number" in str(context.exception))

    def test_should_raise_error_when_function_with_0_arguments_take_some(self):
        with self.assertRaises(ValueError) as context:
            curried_f = curry_explicit(lambda: print("Hello world!"), 0)
            curried_f(1)

        self.assertTrue("Curried function with null arity must not have arguments" in str(context.exception))

    def test_should_raise_error_when_calling_uncurried_function_with_less_arguments_then_passed_arity_is(self):
        with self.assertRaises(ValueError) as context:
            uncurried_function = uncurry_explicit(lambda x: lambda y: x + y, 3)
            result = uncurried_function(1, 2)

        self.assertTrue("Arity is bigger than passed arguments number" in str(context.exception))

    def test_should_raise_error_when_calling_uncurried_function_with_more_arguments_then_passed_arity_is(self):
        with self.assertRaises(ValueError) as context:
            uncurried_function = uncurry_explicit(lambda x: lambda y: x + y, 1)
            result = uncurried_function(1, 2)

        self.assertTrue("Arity is smaller than passed arguments number" in str(context.exception))

    def test_should_raise_error_when_calling_curried_function_with_more_than_one_argument(self):
        with self.assertRaises(ValueError) as context:
            curried_function = curry_explicit(lambda x, y: x + y, 2)
            curried_function(1, 2)

        self.assertTrue(
            "Curried function with non null arity must have only one argument on each step" in str(context.exception)
        )

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

    def test_should_uncurry_function_with_2_arguments(self):
        def f(arg1: int, arg2: int):
            return arg1 + arg2

        curried_f = curry_explicit(f, 2)
        uncurried_f = uncurry_explicit(curried_f, 2)
        self.assertEqual(10, uncurried_f(3, 7))

    def test_should_curry_built_in_function(self):
        curried_f = curry_explicit(sum, 1)
        self.assertEqual(6, curried_f([1, 2, 3]))

    def test_should_curry_function_with_0_arguments(self):
        def f():
            return 1

        curried_f = curry_explicit(f, 0)
        self.assertEqual(1, curried_f())

    def test_should_uncurry_function_with_0_arguments(self):
        def f():
            return 1

        curried_f = curry_explicit(f, 0)
        uncurried_f = uncurry_explicit(curried_f, 0)
        self.assertEqual(1, uncurried_f())

    def test_should_curry_function_with_args(self):
        def f(arg1: int, arg2: int, *args):
            return sum([arg1, arg2, *args])

        curried_f = curry_explicit(f, 5)
        self.assertEqual(15, curried_f(1)(2)(3)(4)(5))
