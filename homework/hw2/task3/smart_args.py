import functools
from inspect import signature


class Isolated:
    def __init__(self, arg):
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
        print(args)
        result = func(*args, **kwargs)
        return result

    return inner


@smart_args
def test(dict):
    dict["a"] = 0
    return dict


if __name__ == "__main__":
    dict = {"a": 10}
    print(test(dict))
    print(dict)
