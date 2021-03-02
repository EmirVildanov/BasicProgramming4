import functools
from inspect import signature, getfullargspec
from copy import deepcopy


# Типа если агрумент по умолчанию Isolated, то его надо скопировать, а не использовать переданный
# Если Evaluated, то его надо зафиксировать
import random


class Isolated:
    def __init__(self, arg=None):
        self.arg = arg


class Evaluated:
    def __init__(self, func):
        if len(signature(func).parameters) != 0:
            raise ValueError("Evaluated eat only functions with no arguments")
        self.func = func


def smart_args(func=None):
    if func is None:
        return lambda func: smart_args(func)

    @functools.wraps(func)
    def inner(*args, **kwargs):
        # print(f"Full inspect: {getfullargspec(func)}")
        func_default_isolated_params_names = []
        func_default_evaluated_params_names = []
        for parameter_name, parameter in signature(func).parameters.items():
            if isinstance(parameter.default, Isolated):
                func_default_isolated_params_names.append(parameter_name)
            if (
                isinstance(parameter.default, Evaluated)
                and parameter_name not in kwargs.keys()
            ):
                func_default_evaluated_params_names.append(parameter_name)
                kwargs[parameter_name] = parameter.default.func()
        for kwarg_name, kwarg in kwargs.items():
            if kwarg_name in func_default_isolated_params_names:
                kwargs[kwarg_name] = deepcopy(kwargs[kwarg_name])
        # print(f"Function_call args: {args}")
        if len(args) != 0:
            args = list(args)
            for i, arg in enumerate(args):
                if isinstance(arg, Evaluated):
                    args[i] = args[i].func()
            args = tuple(args)
        result = func(*args, **kwargs)
        return result

    return inner


@smart_args
def test(*, dict=Isolated()):
    dict["a"] = 0
    return dict


def get_random_number():
    return random.randint(0, 100)


@smart_args
def check_evaluation(*, x=get_random_number(), y=Evaluated(get_random_number)):
    print(x, y)


@smart_args
def check_position(a, b, c=10):
    a[0] = 1
    print(f"{a} {b} {c}")


@smart_args
def function(a, b, c=10):
    print(f"{a} {b} {c}")


if __name__ == "__main__":
    test_dict = {"a": 10}
    print(test(dict=test_dict))
    print(test_dict)
    check_evaluation()
    check_evaluation()
    check_evaluation()
    check_evaluation(y=150)
    # check_position(Evaluated(get_random_number), b=2)
    # check_position(Isolated(), b=2)
