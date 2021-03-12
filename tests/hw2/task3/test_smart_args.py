import unittest
import datetime
from time import sleep

from homework.hw2.task3.smart_args import smart_args, Isolated, Evaluated


def get_date():
    return datetime.datetime.now()


class SmartArgsTestCase(unittest.TestCase):
    def test_should_raise_exception_when_Evaluated_gets_Isolated_as_argument(self):
        with self.assertRaises(ValueError) as context:

            @smart_args
            def function(*, x=get_date(), y=Evaluated(Isolated())):
                return x, y

        self.assertTrue("Isolated argument is not supported by Evaluated" in str(context.exception))

    def test_should_raise_exception_when_Isolated_gets_Evaluated_as_argument(self):
        with self.assertRaises(ValueError) as context:

            @smart_args
            def function(*, x=get_date(), y=Isolated(Evaluated(get_date))):
                return x, y

        self.assertTrue("Evaluated argument is not supported by Isolated" in str(context.exception))

    def test_should_raise_exception_when_function_with_arguments_is_passed_to_Evaluated(self):
        with self.assertRaises(ValueError) as context:

            @smart_args
            def check_evaluation(*, x=get_date(), y=Evaluated(lambda x: x)):
                return x, y

        self.assertTrue("Only functions with no arguments are supported by Evaluated" in str(context.exception))

    def test_should_test_Evaluated_works_properly_with_date_function(self):
        @smart_args
        def check_evaluation(*, x=get_date(), y=Evaluated(get_date)):
            return x, y

        _, date1 = check_evaluation()
        sleep(0.1)
        _, date2 = check_evaluation()
        self.assertTrue(date1 < date2)

    def test_should_test_Evaluated_works_properly_with_decorator_used_with_braces(self):
        @smart_args()
        def check_evaluation(*, x=get_date(), y=Evaluated(get_date)):
            return x, y

        _, date1 = check_evaluation()
        sleep(0.1)
        _, date2 = check_evaluation()
        self.assertTrue(date1 < date2)

    def test_should_Isolate_passed_list_argument(self):
        @smart_args
        def do_operation_over_list(*, test_list=Isolated()):
            test_list[0] = -1

        initial_list = [1]
        do_operation_over_list(test_list=initial_list)
        self.assertEqual(1, initial_list[0])

    def test_should_Isolate_passed_dict_argument(self):
        @smart_args
        def do_operation_over_dict(*, test_dict=Isolated()):
            test_dict["a"] = 1

        initial_dict = {"a": 10}
        do_operation_over_dict(test_dict=initial_dict)
        self.assertEqual(10, initial_dict["a"])

    def test_should_Isolate_positional_argument(self):
        @smart_args(positional_args_on=True)
        def check_position_isolation(a, b, c=10):
            a[0] = 10

        test_list = [1]
        check_position_isolation(Isolated(test_list), b=2)
        self.assertEqual(1, test_list[0])

    def test_should_Evaluate_positional_argument(self):
        @smart_args(positional_args_on=True)
        def check_position_evaluation(a, b, c=10):
            return a

        date1 = check_position_evaluation(Evaluated(get_date), b=2)
        sleep(0.1)
        date2 = check_position_evaluation(Evaluated(get_date), b=2)
        self.assertTrue(date1 < date2)

    def test_should_both_Isolate_and_Evaluate_positional_arguments(self):
        @smart_args(positional_args_on=True)
        def check_position(a, b, c=10):
            b[0] = 10
            return a

        test_list = [1]
        date1 = check_position(Evaluated(get_date), Isolated(test_list))
        sleep(0.1)
        date2 = check_position(Evaluated(get_date), Isolated(test_list))
        self.assertTrue(date1 < date2)

    def test_should_Isolate_both_positional_and_named_arguments(self):
        @smart_args(positional_args_on=True)
        def do_operation_over_list(test_list1, *, test_list2=Isolated()):
            print(test_list1)
            print(test_list2)
            test_list1[0] = -1
            test_list2[0] = -2

        initial_list1 = [1]
        initial_list2 = [1]
        do_operation_over_list(Isolated(initial_list1), test_list2=initial_list2)
        self.assertEqual(1, initial_list1[0])
        self.assertEqual(1, initial_list2[0])
