import functools
import datetime
from collections.abc import Callable, Hashable
from typing import List, Tuple, Generator, Any


class SpyFunction:
    def __init__(self, function: Callable = None):
        if function is None:
            self._function = lambda function: SpyFunction(function)
        else:
            self._function = function
            functools.update_wrapper(self, function)
        self.history: List[Tuple[datetime, List]] = list()

    def __call__(self, *args: Hashable, **kwargs: Hashable):
        arguments_list = list(args)
        for _, v in kwargs.items():
            arguments_list.append(v)
        self.history.append((datetime.datetime.now().__str__(), arguments_list))
        return self._function(*args, **kwargs)


def get_history_generator(history: List[Tuple[Any, list]]) -> Generator:
    for pair in history:
        yield pair


def print_usage_statistic(function: Callable) -> Generator:
    if not isinstance(function, SpyFunction):
        raise TypeError("Function type is not SpyFunction and it doesn't have needed fields ")
    return get_history_generator(function.history)


@SpyFunction
def test_function_with_kwargs(arg1: int, arg2: int, **kwargs) -> int:
    result = 0
    for value in kwargs.values():
        result += value
    return result + arg1 + arg2


if __name__ == "__main__":
    result = test_function_with_kwargs(1, 2, val1=3, val2=4)
    for data, parameters in print_usage_statistic(test_function_with_kwargs):
        print(data, parameters)
