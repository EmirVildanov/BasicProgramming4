import functools
from collections import OrderedDict
from typing import Dict, Tuple, Callable, Any, Hashable


def make_arguments_list(args: Tuple, kwargs: Dict) -> Tuple:
    """
    :param args: *args of passing into decorator function
    :param kwargs: *kwargs of passing into decorator function
    :return: Tuple of constructed arguments list
    """
    full_arguments_list = list(args)
    for k, v in kwargs.items():
        full_arguments_list.append((k, v))
    return tuple(full_arguments_list)


class DecoratorFunction(Callable[[], Any]):
    cash: OrderedDict = None
    function_called_number: int = 0


cash: DecoratorFunction


def cash(func=None, *, n: int = 0) -> Callable:
    """
    :param func: function to decorate
    :param n: maximum size of wanted cash
    :return: inner function
    """
    if func is None:
        return lambda:  cash(func, n=n)

    @functools.wraps(func)
    def inner(*args: Tuple[Hashable], **kwargs: Dict[Hashable, Hashable]):
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
