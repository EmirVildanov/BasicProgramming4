import functools
from collections import OrderedDict
from typing import Dict, Tuple, Callable


def make_arguments_list(args: Tuple, kwargs: Dict) -> Tuple:
    """
    :param args: *args of passing into decorator function
    :param kwargs: *kwargs of passing into decorator function
    :return: Tuple of constructed arguments list
    """
    args = list(args)
    for k, v in kwargs.items():
        args.append((k, v))
    return tuple(args)


def cash(func=None, *, n: int = 0) -> Callable:
    """
    :param func: function to decorate
    :param n: maximum size of wanted cash
    :return: inner function
    """
    if func is None:
        return lambda func: cash(func, n=n)

    @functools.wraps(func)
    def inner(*args, **kwargs):
        if make_arguments_list(args, kwargs) in inner.cash.keys():
            return inner.cash[make_arguments_list(args, kwargs)]
        arguments = make_arguments_list(args, kwargs)
        result = func(*args, **kwargs)
        inner.function_called_number += 1
        if len(inner.cash) > n:
            inner.cash.popitem(last=False)
        if n != 0:
            inner.cash.update({tuple(arguments): result})
        return result

    inner.cash = OrderedDict()
    inner.function_called_number = 0
    return inner
