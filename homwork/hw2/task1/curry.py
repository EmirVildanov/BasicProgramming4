from collections import Callable
from inspect import signature
from typing import List


def check_arity(function: Callable, arity: int):
    """
    :param function: function for checking arity
    :param arity: int value of wanted function arity
    :raises valueError: if arity is negative or incompatible with passed function
    :return: None
    """
    if arity < 0:
        raise ValueError("Arity can not be negative")
    has_args = False
    fun_parameters = signature(function).parameters
    fun_parameters_number = len(fun_parameters)
    if "args" in fun_parameters:
        has_args = True
    if not has_args:
        if fun_parameters_number < arity:
            raise ValueError("Arity is bigger than fun arguments number")
        elif fun_parameters_number > arity:
            raise ValueError("Arity is smaller than fun arguments number")
    elif arity < fun_parameters_number - 1:
        raise ValueError("Arity is smaller than positional functions arguments number")


def curry_explicit(function: Callable, arity: int, passed_args: List = None):
    """
    :param function: function that should be curried
    :param arity: int value of wanted function arity
    :param passed_args: arguments that are wanted to be splitted
    :raises valueError: if arity is negative or incompatible with passed function
    :return: None
    """
    check_arity(function, arity)
    if passed_args is None:
        passed_args = []

    def curried_function(*args):
        if arity != 0 and len(args) != 1:
            raise ValueError("Function with non null arity must have only one argument")
        cur_args = [*passed_args, *args]
        if len(cur_args) < arity:
            return curry_explicit(function, arity, cur_args)
        elif len(cur_args) == arity:
            return function(*cur_args)
        else:
            raise ValueError("Too many arguments")

    return curried_function


def uncurry_explicit(function: Callable, arity: int):
    """
    :param function: function that should be uncurried
    :param arity: int value of wanted function arity
    :raises valueError: if arity is incompatible with passed function
    :return: None
    """
    if arity < 0:
        raise ValueError("Arity can not be negative")

    def uncurried_function(*args):
        if len(args) < arity:
            raise ValueError("Arity is bigger than passed arguments number")
        elif len(args) > arity:
            raise ValueError("Arity is smaller than passed arguments number")
        args = list(args)
        result = function
        while len(args) != 0:
            result = result(args[0])
            del args[0]
        return result

    return uncurried_function


if __name__ == "__main__":
    try:
        f2 = curry_explicit((lambda x, y: f"<{x},{y}>"), 2)
        g2 = uncurry_explicit(f2, 2)
        print(f2(123)(456))
        print(g2(123, 456))
    except ValueError:
        print("Check the passing arity")
