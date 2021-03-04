import functools
from collections.abc import Callable
from inspect import signature, getfullargspec
from copy import deepcopy
import random


class Isolated:
    def __init__(self, arg=None):
        """
        :param arg: argument passing for smart_args
        :raises valueError in case Evaluated is passed inside
        """
        if isinstance(arg, Evaluated):
            raise ValueError("Evaluated argument is not supported by Isolated")
        self.arg = arg


class Evaluated:
    def __init__(self, func):
        """
        :param func: func passing for smart_args
        :raises valueError in case Isolated is passed inside
        """
        if isinstance(func, Isolated):
            raise ValueError("Isolated argument is not supported by Evaluated")
        if len(signature(func).parameters) != 0:
            raise ValueError("Only functions with no arguments are supported by Evaluated")
        self.func = func


def smart_args(func=None, *, positional_args_on: bool = False) -> Callable:
    """
    :param func: inner function for decorator
    :param positional_args_on: if True decorator will also watch through positional arguments
    :return: inner function with processed Isolated and Evaluated arguments
    """
    if func is None:
        if positional_args_on:
            return lambda func: smart_args(func, positional_args_on=True)
        return lambda func: smart_args(func)

    @functools.wraps(func)
    def inner(*args, **kwargs):
        func_default_isolated_params_names = []
        func_default_evaluated_params_names = []
        for parameter_name, parameter in signature(func).parameters.items():
            if isinstance(parameter.default, Isolated):
                func_default_isolated_params_names.append(parameter_name)
            if isinstance(parameter.default, Evaluated) and parameter_name not in kwargs.keys():
                func_default_evaluated_params_names.append(parameter_name)
                kwargs[parameter_name] = parameter.default.func()
        for kwarg_name, kwarg in kwargs.items():
            if kwarg_name in func_default_isolated_params_names:
                kwargs[kwarg_name] = deepcopy(kwargs[kwarg_name])
        if positional_args_on and len(args) != 0:
            args = list(args)
            for i, arg in enumerate(args):
                if isinstance(arg, Isolated):
                    args[i] = deepcopy(arg.arg)
                if isinstance(arg, Evaluated):
                    args[i] = args[i].func()
        return func(*tuple(args), **kwargs)

    return inner
