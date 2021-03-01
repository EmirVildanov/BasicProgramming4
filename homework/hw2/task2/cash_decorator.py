import functools
from collections import OrderedDict
from typing import List, Dict, Tuple, Callable


def make_arguments_list(args: Tuple, kwargs: Dict):
    args = tuple(args)
    for k, v in kwargs:
        args.append((k, v))
    return args


def check_if_in_arguments_list(arguments_list, args: Tuple, kwargs: Dict):
    for element in args:
        if element not in arguments_list:
            return False
    for k, v in kwargs:
        if (k, v) not in arguments_list:
            return False
    return True


def cash(func=None, arguments_cash=OrderedDict(), *, n: int) -> Callable:
    if func is None:
        return lambda func: cash(func, n=n)

    @functools.wraps(func)
    def inner(*args, **kwargs):
        if make_arguments_list(args, kwargs) in arguments_cash.keys():
            print("Returned from cash")
            return arguments_cash[make_arguments_list(args, kwargs)]
        arguments = make_arguments_list(args, kwargs)
        result = func(*args, **kwargs)
        if len(arguments_cash) > n:
            print(f"Had to delete {arguments_cash.popitem(last=False)}")
        else:
            print(f"Len of arg_cash: {len(arguments_cash)}")
        arguments_cash.update({tuple(arguments): result})
        return result

    return inner


@cash(n=3)
def sum(a: int, b: int):
    return a + b


if __name__ == "__main__":
    result = sum(1, 2)
    print(result)
    result1 = sum(1, 2)
    print(result1)
    for i in range(5):
        result3 = sum(1, i)
        print(result3)
