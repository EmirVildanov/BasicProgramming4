import functools
import inspect
from collections.abc import Callable, Hashable


class TakesFunction:
    def __init__(self, *args):
        # if decorator called with braces
        if len(args) != 0 and not (isinstance(args[0], Callable) and not inspect.isclass(args[0])):
            self._function = lambda function: TakesFunction(function, *args)
            self._types_list = args
        else:
            self._function = args[0]
            self._types_list = args[1:]
            functools.update_wrapper(self, args[0])

    def __call__(self, *args: Hashable, **kwargs: Hashable):
        if isinstance(args[0], Callable) and not inspect.isclass(args[0]):
            return self._function(*args, **kwargs)
        for index, parameter_type in enumerate(self._types_list):
            if index < len(args):
                if not isinstance(args[index], parameter_type):
                    raise TypeError(
                        f"Passed parameter type is invalid. Needed {parameter_type}, was {args[index].__class__}. "
                        f"Index - {index} "
                    )
            elif index - len(args) < len(kwargs.values()):
                if not isinstance(list(kwargs.values())[index - len(args)], parameter_type):
                    raise TypeError(
                        f"Passed parameter type is invalid. Needed {parameter_type}, was {list(kwargs.values())[index - len(args)].__class__} Index - {index} "
                    )
        result = self._function(*args, **kwargs)
        return result


@TakesFunction(int, int)
def test_function(a, b):
    print(f"Successful call with a={a} and b={b}")


@TakesFunction(int, int, str, int)
def test_function_with_kwargs(a, b, **kwargs):
    print(f"Successful call with a={a} and b={b}, and kwargs={kwargs}")


if __name__ == "__main__":
    test_function_with_kwargs(1, 1, val1="4", val2=5)
