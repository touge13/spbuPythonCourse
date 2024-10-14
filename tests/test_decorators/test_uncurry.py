import pytest
from project.decorators.curry import curry_explicit
from project.decorators.uncurry import uncurry_explicit

# uncurry tests
def test_uncurry_basic():
    f2 = curry_explicit(lambda x, y, z: f'<{x},{y}, {z}>', 3)
    g2 = uncurry_explicit(f2, 3)
    assert g2(1, 2, 3) == '<1,2, 3>'

def test_uncurry_arity_mismatch():
    f = curry_explicit(lambda x, y: x + y, 2)
    g = uncurry_explicit(f, 2)
    with pytest.raises(TypeError):
        g(1) # Not enough arguments
