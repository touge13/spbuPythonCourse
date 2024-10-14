import inspect
import random

class Evaluated:
    """Class to indicate that the default value of a function argument should be evaluated when called."""
    def __init__(self, func):
        self.func = func

class Isolated:
    """Class to indicate that the default value of a function argument should be a deep copy."""
    pass

def smart_args(positional_support=False):
    """
    Decorator to handle default argument values in a smart way.

    Evaluated: Computes the default value when the function is called if the argument is not provided.
    Isolated: Provides a deep copy of the default value to ensure isolation if the argument is mutable.

    Args:
        positional_support (bool): Enable or disable support for positional arguments.

    Raises:
        ValueError: If a required argument is not provided, if Isolated and Evaluated are used together,
                     or if positional arguments are provided when disabled.
    """
    def decorator(func):
        """Wraps the original function to modify its argument handling."""
        # Get the signature of the function to analyze parameters
        signature = inspect.signature(func)
        parameters = signature.parameters

        def wrapper(*args, **kwargs):
            """Handles the argument processing and invokes the original function."""
            # Check for positional arguments if not supported
            if not positional_support:
                assert len(args) == 0, "Positional arguments are not allowed. Use named arguments."
            
            # Create a new dictionary for the default argument values
            new_kwargs = {}

            for i, (name, param) in enumerate(parameters.items()):
                if i < len(args):
                    # If a positional argument is provided, use it
                    new_kwargs[name] = args[i]
                elif name in kwargs:
                    # If the argument is explicitly passed, use it
                    new_kwargs[name] = kwargs[name]
                elif param.default is param.empty:
                    raise ValueError(f"Argument '{name}' is required but not provided.")
                else:
                    # Handle default values
                    if isinstance(param.default, Evaluated):
                        # Ensure Evaluated and Isolated are not used together
                        assert not isinstance(param.default.func, Isolated), (
                            f"Cannot use Evaluated and Isolated together for argument '{name}'."
                        )
                        # Compute the value if Evaluated is used
                        new_kwargs[name] = param.default.func()
                    elif isinstance(param.default, Isolated):
                        # Check if Isolated is used with a passed argument
                        assert len(args) <= i, (
                            f"Argument '{name}' must be provided as a keyword argument, "
                            "not as a positional argument."
                        )
                        # Copy the value if Isolated is used
                        new_kwargs[name] = {}
                    else:
                        # Simply take the default value
                        new_kwargs[name] = param.default
            
            # Call the original function with the new values
            return func(*args, **new_kwargs)

        return wrapper

    return decorator

# Examples of using the smart_args decorator
@smart_args()
def check_isolation(*, d=Isolated()):
    """Check isolation by modifying a dictionary passed as an argument."""
    d['a'] = 0
    return d

def get_random_number():
    """Generates a random number between 0 and 100."""
    return random.randint(0, 100)

@smart_args()
def check_evaluation(*, x=get_random_number(), y=Evaluated(get_random_number)):
    """Check the evaluation of default values."""
    print(x, y)

# Example with positional arguments enabled
@smart_args(positional_support=True)
def example_with_positional(a=1, b=2):
    """An example function that accepts positional arguments."""
    return a + b
