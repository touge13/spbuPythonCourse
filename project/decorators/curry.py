def curry_explicit(function, arity):
    """
    Curries the given function to the specified arity.
    
    Arguments:
    function -- The original function to be curried.
    arity -- The number of arguments the function takes.
    
    Returns:
    A curried version of the function.
    
    Raises:
    ValueError -- If arity is negative.
    TypeError -- If more arguments are provided than the arity allows.
    """
    if arity < 0:
        raise ValueError("Arity cannot be negative")
    if arity == 0:
        return lambda: function()

    def curried(*args):
        if len(args) > arity:
            raise TypeError(f"Expected {arity} arguments, but got {len(args)}")
        if len(args) == arity:
            return function(*args)
        return lambda *new_args: curried(*(args + new_args))

    return curried

