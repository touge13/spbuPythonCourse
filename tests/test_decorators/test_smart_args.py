from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from project.decorators.smart_args import (
    smart_args,
    Evaluated,
    Isolated,
    get_random_number,
)

import pytest


def test_evaluated():
    """Test Evaluated handling in the function."""

    @smart_args(allow_positional=False)
    def test_func(*, x=Evaluated(lambda: 0)):  # Use a lambda to return a fixed value
        return x

    result = test_func()
    assert result == 0  # Now it should always return 0


def test_isolated():
    """Test Isolated handling in the function."""

    @smart_args()
    def test_func(*, d=Isolated()):
        return d

    result = test_func()
    assert isinstance(result, dict)  # Should return a new dictionary
    assert result == {}  # Initial value of the dictionary should be empty

    # Modify the returned dictionary to check isolation
    result["a"] = 1
    assert result["a"] == 1  # Check if the modification is successful

    # Call the function again to ensure isolation
    result2 = test_func()
    assert result2 == {}  # Should return a new, separate dictionary


def test_isolated_and_evaluated_in_combination():
    """Test the combination of Isolated and Evaluated, which should raise an assertion error."""

    @smart_args()
    def test_func(*, d=Isolated(), y=Evaluated(lambda: 0)):
        return d, y

    assert test_func()


def test_isolated_with_positional_argument():
    """Test Isolated handling with positional arguments."""

    @smart_args(allow_positional=True)
    def test_func(d=Isolated()):
        return d

    result = test_func()
    assert isinstance(result, dict)  # Should return a new dictionary
    assert result == {}  # Initial value of the dictionary should be empty

    # Modify the returned dictionary to check isolation
    result["a"] = 1
    assert result["a"] == 1  # Check if the modification is successful


def test_evaluated_with_positional_argument():
    """Test Evaluated handling with positional arguments."""

    @smart_args(allow_positional=True)
    def test_func(x=Evaluated(get_random_number)):
        return x

    result = test_func(10)  # Positional argument passed
    assert result == 10  # Positional argument should take precedence


def test_default_behavior_without_arguments():
    """Test that default values are correctly returned when no arguments are passed."""

    @smart_args()
    def test_func(*, d=Isolated()):
        return d

    result = test_func()
    assert isinstance(result, dict)  # Should return a new dictionary
    assert result == {}  # Initial value of the dictionary should be empty


def test_mixed_arguments_with_evaluated():
    """Test that using positional and keyword arguments with Evaluated works as expected."""

    @smart_args(allow_positional=True)
    def test_func(x=Evaluated(get_random_number), y=0):
        return x, y

    result = test_func(1)  # Using positional argument
    assert result == (1, 0)  # Should return positional argument and default for y
