import pytest
import random
from project.decorators.smart_args import (
    smart_args, Evaluated, Isolated, 
    check_isolation, check_evaluation, 
    example_with_positional, get_random_number
)

def test_check_isolation():
    """Test for the Isolated behavior."""
    no_mutable = {'a': 10}
    result = check_isolation(d=no_mutable)
    
    assert result['a'] == 0  # Check if the returned dictionary has been modified
    assert no_mutable['a'] == 10  # Ensure the original dictionary remains unchanged

    result2 = check_isolation()
    assert result2['a'] == 0  # Check if a new isolated dictionary is returned
    assert 'a' not in result2  # Ensure isolation is correct

def test_check_evaluation():
    """Test for the Evaluated behavior."""
    random.seed(0)  # Seed for reproducibility
    
    # First call - should compute default values
    result1 = check_evaluation()
    
    assert isinstance(result1, tuple) and len(result1) == 2  # Check result is a tuple
    x1, y1 = result1
    assert y1 != x1  # Ensure y is different from x

    # Second call - should produce different y
    result2 = check_evaluation()
    
    assert y1 != result2[1]  # Check y has changed
    assert result2[0] == x1  # Ensure x remains the same
    
    # Calling with a specific value for y
    result3 = check_evaluation(y=150)
    
    assert result3[1] == 150  # Ensure y is set to the specified value

def test_isolated_and_evaluated_together():
    """Test that using Isolated and Evaluated together raises an assertion error."""
    @smart_args
    def faulty_func(*, a=Isolated(), b=Evaluated(get_random_number)):
        return a, b

    with pytest.raises(AssertionError, match="Cannot use Evaluated and Isolated together for argument 'b'."):
        faulty_func()

def test_positional_arguments_not_allowed():
    """Test that using positional arguments when disabled raises an assertion error."""
    no_mutable = {'a': 10}  # Define no_mutable within the test function

    with pytest.raises(AssertionError, match="Positional arguments are not allowed. Please use named arguments."):
        check_isolation(d=no_mutable)  # Pass d as a keyword argument

    with pytest.raises(AssertionError, match="Positional arguments are not allowed. Please use named arguments."):
        check_evaluation(y=5)  # This should fail since it's a positional argument

def test_example_with_positional():
    """Test example function that allows positional arguments."""
    assert example_with_positional(3, 4) == 7  # Test positional arguments
    assert example_with_positional() == 3  # Test defaults
