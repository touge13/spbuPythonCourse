from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from project.decorators.smart_args import (
    smart_args,
    Evaluated,
    Isolated,
    check_isolation,
    check_evaluation,
    example_with_positional,
    get_random_number,
)


def test_check_isolation():
    d1 = check_isolation(d={})
    d2 = check_isolation(d={})
    assert d1 is not d2, "Each call should return a different dictionary."
    assert d1["a"] == 0 and d2["a"] == 0, "The value of 'a' should be modified to 0."


def test_check_evaluation():
    x = get_random_number()
    y = get_random_number()
    result = check_evaluation()  # Call without arguments
    assert result[0] == x, f"x should be {x}."
    assert result[1] == y, f"y should be {y}."


def test_example_with_positional():
    assert example_with_positional(3, 4) == 7
    assert example_with_positional(b=3, a=4) == 7
    assert example_with_positional() == 3
    assert example_with_positional(10) == 12


def test_evaluated_and_isolated_combined():
    with pytest.raises(AssertionError):

        @smart_args()
        def test_function(*, x=Evaluated(get_random_number), d=Isolated()):
            pass

        assert test_function()


def test_required_argument_not_provided():
    with pytest.raises(ValueError):

        @smart_args()
        def test_function(*, required_arg):
            return required_arg

        test_function()
