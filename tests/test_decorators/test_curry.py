from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from project.decorators.curry import curry_explicit

# curry tests
def test_curry_basic():
    f2 = curry_explicit(lambda x, y, z: f'<{x},{y}, {z}>', 3)
    assert f2(1)(2)(3) == '<1,2, 3>'

def test_curry_arity_1():
    f = curry_explicit(lambda x: x * 2, 1)
    assert f(5) == 10

def test_curry_arity_0():
    f = curry_explicit(lambda: "Hello, World!", 0)
    assert f() == "Hello, World!"

def test_curry_type_error():
    f = curry_explicit(lambda x, y: x + y, 2)
    with pytest.raises(TypeError):
        f(1)(2)(3) # Extra argument

def test_negative_arity():
    with pytest.raises(ValueError):
        curry_explicit(lambda x: x, -1)

def test_curry_proper_usage():
    f = curry_explicit(lambda x, y, z: f'{x} {y} {z}', 3)
    assert f(1)(2)(3) == '1 2 3'
    assert f(1)(2)(0) == '1 2 0'
