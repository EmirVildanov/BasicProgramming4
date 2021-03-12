import functools
from collections import OrderedDict
from typing import Dict, Tuple, Callable, Hashable


def make_arguments_list(args: Tuple, kwargs: Dict) -> Tuple:
    """
    :param args: *args of passing into decorator function
    :param kwargs: *kwargs of passing into decorator function
    :return: Tuple of constructed arguments list
    """
    full_arguments_list = list(args)
    for k, v in sorted(kwargs.items()):
        full_arguments_list.append((k, v))
    return tuple(full_arguments_list)


class FunctionWithCache:
    def __init__(self, function: Callable = None, cache_size: int = 0):
        """
        :param function: function to decorate
        :param cache_size: maximum size of wanted cache
        """
        if function is None:
            self._function = lambda function: FunctionWithCache(function, cache_size=cache_size)
        else:
            self._function = function
            functools.update_wrapper(self, function)
        self._cache: OrderedDict = OrderedDict()
        self._cache_size = cache_size
        self._function_called_number = 0

    def __call__(self, *args: Hashable, **kwargs: Hashable):
        if make_arguments_list(args, kwargs) in self._cache.keys():
            return self._cache[make_arguments_list(args, kwargs)]
        arguments = make_arguments_list(args, kwargs)
        result = self._function(*args, **kwargs)
        self._function_called_number += 1
        if len(self._cache) > self._cache_size:
            self._cache.popitem(last=False)
        if self._cache_size != 0:
            self._cache.update({tuple(arguments): result})
        return result
