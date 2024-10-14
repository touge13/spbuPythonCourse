from collections import OrderedDict
from functools import wraps


def cache_results(max_cache_size=0):
    """Decorator to cache function results.

    Args:
        max_cache_size (int): The maximum number of results to cache.
                               Default is 0, which means no caching.

    Returns:
        function: The wrapped function with caching behavior.
    """

    def decorator(func):
        cache = OrderedDict()  # Using OrderedDict to maintain insertion order

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create a cache key based on the function arguments
            key = (args, frozenset(kwargs.items()))

            # Check if the result is already in the cache
            if key in cache:
                return cache[key]

            # Call the function and cache the result
            result = func(*args, **kwargs)
            cache[key] = result

            # Remove the oldest item if the cache exceeds the max size
            if max_cache_size > 0 and len(cache) > max_cache_size:
                cache.popitem(last=False)  # Remove the oldest item

            return result

        return wrapper

    return decorator


# Example function
@cache_results(max_cache_size=3)
def expensive_computation(x, y=0):
    """Simulates an expensive computation.

    Args:
        x (int): First parameter.
        y (int, optional): Second parameter. Defaults to 0.

    Returns:
        int: The sum of x and y.
    """
    print(f"Computing result for ({x}, {y})")
    return x + y
