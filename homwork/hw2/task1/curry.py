import inspect
from inspect import signature


def test_function(arg1: int, arg2: str, arg3: str, *args):
    return f"{arg1} {arg2} {arg3} {[arg for arg in args]}"


# print(signature(function))
# print(type(signature(function)))
# print(signature(function).parameters)
# print(len(signature(function).parameters))


def curry_explicit(function, arity):
    if 'args' in signature(function).parameters:
        function_named_args_number = len(signature(function).parameters) - 1
    else:
        function_named_args_number = len(signature(function).parameters)
    if arity < 0:
        raise ValueError("Negative arity")
    elif arity < function_named_args_number:
        raise ValueError("Passed wrong arity")
    elif arity == 0:
        return function
    elif arity == 1:
        return lambda x: function(x)
    else:
        return curry_explicit(function, arity - 1)


def curry(fun, arity, passed_args=None):
    if passed_args is None:
        passed_args = [] # как бы глубже и глубже передаём наши агрументы до тех пор, пока
        # переданные прежде в сумме с переданным в конце по длине не равны arity

    def wrapper(*args):
        cur_args = [*passed_args, *args]
        if len(cur_args)< arity:
            return curry(fun, arity, cur_args)
        elif len(cur_args) == arity:
            return fun(*cur_args)
        else:
            "too many args"
    return wrapper


def uncurry_explicit(function, arity):
    if arity < 0:
        raise ValueError("Negative arity")
    if arity == 0:
        return function()
    elif arity == 1:
        return lambda x: function(x)
    elif arity == 2:
        return lambda x, y: function(x)(y)


if __name__ == "__main__":
    try:
        test = curry(test_function, 3)
        print(test(1)(2)(3)(4))
        # f2 = curry_explicit((lambda x, y: f'<{x},{y}>'), 2)
        # g2 = uncurry_explicit(f2, 2)
        # print(f2(123)(456))
        # print(g2(123, 456))
    except ValueError:
        print("Check the passing arity")