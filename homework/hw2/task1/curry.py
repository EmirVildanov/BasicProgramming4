import types
from collections.abc import Callable
from inspect import signature, getfullargspec
from typing import List

NEGATIVE_ARITY_ERROR_MESSAGE = "Arity can not be negative"
BIGGER_ARITY_ERROR_MESSAGE = "Arity is bigger than fun arguments number"
SMALLER_ARITY_ERROR_MESSAGE = "Arity is smaller than fun arguments number"
POSITIONAL_ARGS_ARITY_INCOMPATIBILITY_ERROR_MESSAGE = "Arity is smaller than positional functions arguments number"
FUNC_MULTIPLE_ARGS_ERROR_MESSAGE = "Curried function with non null arity must have only one argument on each step"
ZERO_ARITY_ARGS_ERROR_MESSAGE = "Curried function with null arity must not have arguments"


def check_arity_for_positional_parameters(arguments_number: int, arity: int):
    if arguments_number < arity:
        raise ValueError(BIGGER_ARITY_ERROR_MESSAGE)
    elif arguments_number > arity:
        raise ValueError(SMALLER_ARITY_ERROR_MESSAGE)


def check_arity(function: Callable, arity: int):
    """
    :param function: function for checking arity
    :param arity: int value of wanted function arity
    :raises valueError: if arity is negative or incompatible with passed function
    :return: None
    """
    if arity < 0:
        raise ValueError(NEGATIVE_ARITY_ERROR_MESSAGE)
    if isinstance(function, types.BuiltinFunctionType):
        return
    fun_parameters = signature(function).parameters
    fun_parameters_number = len(fun_parameters)
    if getfullargspec(function).varargs is None:
        check_arity_for_positional_parameters(fun_parameters_number, arity)
    elif arity < fun_parameters_number - 1:
        raise ValueError(POSITIONAL_ARGS_ARITY_INCOMPATIBILITY_ERROR_MESSAGE)


def curry_explicit(function: Callable, arity: int, passed_args: List = None) -> Callable:
    """
    :param function: function that should be curried
    :param arity: int value of wanted function arity
    :param passed_args: arguments that are wanted to be splitted
    :raises valueError: if arity is negative or incompatible with passed function
    :return: curried function
    """
    check_arity(function, arity)
    passed_args = passed_args or []

    def curried_function(*args):
        if arity != 0 and len(args) != 1:
            raise ValueError(FUNC_MULTIPLE_ARGS_ERROR_MESSAGE)
        elif arity == 0 and len(args) != 0:
            raise ValueError(ZERO_ARITY_ARGS_ERROR_MESSAGE)
        cur_args = [*passed_args, *args]
        if len(cur_args) < arity:
            return curry_explicit(function, arity, cur_args)
        elif len(cur_args) == arity:
            return function(*cur_args)

    return curried_function


def uncurry_explicit(function: Callable, arity: int) -> Callable:
    """
    :param function: function that should be uncurried
    :param arity: int value of wanted function arity
    :raises valueError: if arity is incompatible with passed function
    :return: uncurried function
    """
    if arity < 0:
        raise ValueError(NEGATIVE_ARITY_ERROR_MESSAGE)

    def uncurried_function(*args):
        check_arity_for_positional_parameters(len(args), arity)
        args = list(args)
        if arity == 0:
            return function()
        result = function
        while len(args) != 0:
            result = result(args[0])
            del args[0]
        return result

    return uncurried_function
