from inspect import signature


def check_arity(fun, arity):
    has_args = False
    fun_parameters = signature(fun).parameters
    fun_parameters_number = len(fun_parameters)
    if "args" in fun_parameters:
        has_args = True
    if not has_args:
        if fun_parameters_number < arity:
            raise ValueError("Arity is bigger than fun arguments number")
        elif fun_parameters_number > arity:
            raise ValueError("Arity is smaller than fun arguments number")
    elif arity < fun_parameters_number - 1:
        raise ValueError("Arity is smaller than named functions arguments number")


def curry_explicit(fun, arity, passed_args=None):
    if arity < 0:
        raise ValueError("Arity can not be negative")
    check_arity(fun, arity)
    if passed_args is None:
        passed_args = []

    def wrapper(*args):
        if arity != 0 and len(args) != 1:
            raise ValueError("Function with non null arity must have only one argument")
        cur_args = [*passed_args, *args]
        if len(cur_args) < arity:
            return curry_explicit(fun, arity, cur_args)
        elif len(cur_args) == arity:
            return fun(*cur_args)
        else:
            raise ValueError("Too many arguments")

    return wrapper


def uncurry_explicit(function, arity):
    def returning_lambda(*args):
        if len(args) < arity:
            raise ValueError("Arity is bigger than passed arguments number")
        elif len(args) > arity:
            raise ValueError("Arity is smaller than passed arguments number")
        args = list(args)
        result = function
        while len(args) != 0:
            result = result(args[0])
            del args[0]
        return result

    return returning_lambda


if __name__ == "__main__":
    try:
        f2 = curry_explicit((lambda x, y: f"<{x},{y}>"), 2)
        g2 = uncurry_explicit(f2, 2)
        print(f2(123)(456))
        print(g2(123, 456))
    except ValueError:
        print("Check the passing arity")
