import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from project.vector_operations import Vector

# Fixtures
@pytest.fixture
def vector1():
    return Vector([1.5, 2, 3])


@pytest.fixture
def vector2():
    return Vector([4, 5, 6])


# Vector Tests
def test_vector_initialization():
    vec = Vector([1.5, 2, 3])
    assert vec.vector == [1.5, 2, 3], "Vector initialization failed"


def test_vector_dot_product(vector1, vector2):
    assert vector1 * vector2 == 34.0, f"Expected 34.0, got {vector1 * vector2}"


def test_vector_length(vector1):
    assert len(vector1) == 3, f"Expected length 3, got {len(vector1)}"


def test_vector_norm():
    v = Vector([1.5, 2])
    assert abs(v.norm() - 2.5) < 1e-7, f"Expected norm 2.5, got {v.norm()}"


def test_vector_angle():
    v1 = Vector([1, 0])
    v2 = Vector([0, 1])
    angle = v1 ^ v2
    assert (
        abs(angle - (3.141592653589793 / 2)) < 1e-7
    ), f"Expected angle π/2, got {angle}"


def test_zero_vector_norm():
    v = Vector([0, 0, 0])
    with pytest.raises(ZeroDivisionError):
        v ^ v  # This should raise ZeroDivisionError
