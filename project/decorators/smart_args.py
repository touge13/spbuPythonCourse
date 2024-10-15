import copy
import inspect


class Evaluated:
    """Wrapper for evaluated default values. Expects a callable function."""

    def __init__(self, func):
        assert callable(func), "Evaluated expects a callable"
        self.func = func


class Isolated:
    """Placeholder for isolated default values that should be deeply copied."""

    pass


def smart_args(allow_positional=False):
    """
    Decorator to handle 'Evaluated' and 'Isolated' argument defaults.

    Args:
    allow_positional (bool): If True, positional arguments are allowed.
                             Otherwise, only keyword arguments are supported.

    This decorator processes arguments with specific behavior:
    - Evaluated(func): A default value that is evaluated at the time of function call.
    - Isolated(): A placeholder that requires deep copying of the passed argument.

    Raises:
    - AssertionError: If both Evaluated and Isolated are used together.
    - AssertionError: If positional arguments are used while disabled.
    """

    def decorator(func):
        """
        Decorator function that wraps the original function to handle
        'Evaluated' and 'Isolated' argument defaults.

        Args:
            func (callable): The function to be wrapped.

        Returns:
            callable: A wrapper function that processes the arguments before
                    calling the original function.
        """

        def wrapper(*args, **kwargs):
            """
            Wrapper function that processes arguments for the decorated function,
            handling special cases for 'Evaluated' and 'Isolated' argument defaults.

            Args:
                *args: Positional arguments passed to the original function.
                **kwargs: Keyword arguments passed to the original function.

            Raises:
                AssertionError: If positional arguments are provided when not allowed.
                AssertionError: If both 'Evaluated' and 'Isolated' are used for the same argument.
                IndexError: If more positional arguments are provided than expected.

            Returns:
                The result of the original function after processing the arguments.
            """
            # Fetch full argument specification
            full_argspec = inspect.getfullargspec(func)
            defaults = full_argspec.defaults or ()
            kwonly_defaults = full_argspec.kwonlydefaults or {}
            positional_args = full_argspec.args or []
            pos_defaults_offset = len(positional_args) - len(defaults)

            # Check if positional arguments are allowed
            if not allow_positional:
                assert len(args) == 0, "Only keyword arguments are allowed"

            # Process named arguments
            bound_args = kwargs.copy()

            # Apply positional arguments (if allowed)
            for i, arg_value in enumerate(args):
                arg_name = positional_args[i]
                bound_args[arg_name] = arg_value

            # Handle default values for positional arguments
            for i, arg_name in enumerate(positional_args[pos_defaults_offset:]):
                if arg_name not in bound_args:
                    bound_args[arg_name] = defaults[i]

            # Handle keyword-only arguments and apply defaults if necessary
            for kwarg_name, default_value in kwonly_defaults.items():
                if kwarg_name not in bound_args:
                    bound_args[kwarg_name] = default_value

            # Process Evaluated and Isolated
            for name, value in bound_args.items():
                if isinstance(value, Evaluated):
                    bound_args[name] = value.func()  # Evaluate function
                elif isinstance(value, Isolated):
                    # Deep copy only if it's a dict
                    bound_args[name] = copy.deepcopy(kwargs.get(name, {}))  # Deep copy

            # Check for incorrect combination of Evaluated and Isolated
            for name, value in bound_args.items():
                assert not (
                    isinstance(value, Evaluated) and isinstance(value, Isolated)
                ), f"Cannot combine Evaluated and Isolated for argument {name}"

            return func(**bound_args)

        return wrapper

    return decorator


# Example usage
import random


def get_random_number():
    """Function to generate a random number between 0 and 100."""
    random.seed(0)
    return random.randint(0, 100)


@smart_args(allow_positional=False)
def check_evaluation(*, x=get_random_number(), y=Evaluated(get_random_number)):
    """Prints x and y values with Evaluated handling for 'y'."""
    print(x, y)


no_mutable = {"a": 10}


@smart_args()
def check_isolation(*, d=Isolated()):
    """Modifies the dictionary passed by making a deep copy using Isolated."""
    d["a"] = 0
    return d
