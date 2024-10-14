from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from project.decorators.cache_decorator import cache_results, expensive_computation


def test_cache_no_caching():
    """Test the function without caching."""
    result1 = expensive_computation(1)
    assert result1 == 1
    result2 = expensive_computation(1)
    assert result2 == result1  # Cached result should be used
    assert expensive_computation(2) == 2  # New input, should compute


def test_cache_with_size_limit():
    """Test the function with caching and a size limit."""
    cached_function = cache_results(max_cache_size=2)(expensive_computation)

    assert cached_function(1) == 1  # Compute and cache (1, 0)
    assert cached_function(2) == 2  # Compute and cache (2, 0)
    assert cached_function(1) == 1  # Cached result (1, 0)

    # At this point, the cache contains (1, 0) and (2, 0)
    assert cached_function(3) == 3  # Compute and cache (3, 0)

    # Now the cache should contain (2, 0) and (3, 0), (1, 0) should be evicted
    assert cached_function(2) == 2  # Cached result (2, 0)
    assert cached_function(3) == 3  # Cached result (3, 0)

    # Since (1, 0) was evicted, this call should compute again
    assert cached_function(1) == 1  # Should compute again


def test_cache_varied_arguments():
    """Test the function with varied arguments."""
    cached_function = cache_results(max_cache_size=2)(expensive_computation)

    assert cached_function(5, y=10) == 15  # Compute and cache (5, 10)
    assert cached_function(5, y=10) == 15  # Cached result (5, 10)
    assert cached_function(5, y=20) == 25  # Compute and cache (5, 20)

    # Now the cache contains (5, 10) and (5, 20)
    assert cached_function(10) == 10  # Compute and cache (10, 0)

    # (5, 10) is now evicted, since we reached max size
    assert (
        cached_function(5, y=10) == 15
    )  # Should compute again, as (5, 10) was evicted
