import functools
import inspect
from datetime import datetime
from typing import Callable, Hashable


class LoggerFunction:
    def __init__(self, *args):
        if len(args) != 0 and not (isinstance(args[0], Callable) and not inspect.isclass(args[0])):
            if len(args) > 1:
                raise ValueError("Decorator takes only one string [save_file_path] argument")
            elif not isinstance(args[0], str):
                raise ValueError("Decorator takes string [save_file_path] argument")
            self._function = lambda function: LoggerFunction(function, *args)
            self.save_path: str = args[0]
            self.file_was_opened = False
        elif len(args) == 1 and isinstance(args[0], Callable):
            raise ValueError("You can not use this decorator without passing file name")
        else:
            self._function = args[0]
            self.save_path = args[1]
            self.file_was_opened = False
            self.__name__ = args[0].__name__
            functools.update_wrapper(self, args[0])

    def __call__(self, *args: Hashable, **kwargs: Hashable):
        if not inspect.isclass(args[0]):
            return self._function(*args, **kwargs)
        result = self._function(*args, **kwargs)
        if not self.file_was_opened:
            with open(self.save_path, "w") as f:
                f.write(f"{datetime.now()} {self.__name__} {args} ({kwargs}) {result} \n")
            self.file_was_opened = True
        else:
            with open(self.save_path, "a") as f:
                f.write(f"{datetime.now()} {self.__name__} {args} ({kwargs}) {result} \n")
        return result
