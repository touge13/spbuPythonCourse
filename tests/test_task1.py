import pytest
import numpy as np
from project.task1 import Vector, Matrix

# Fixtures
@pytest.fixture
def vector1():
    return Vector([1, 2, 3])


@pytest.fixture
def vector2():
    return Vector([4, 5, 6])


@pytest.fixture
def matrix1():
    return Matrix([[1, 2], [3, 4]])


@pytest.fixture
def matrix2():
    return Matrix([[5, 6], [7, 8]])


# Vector Tests
def test_vector_initialization():
    vec = Vector([1.5, 2, 3])
    assert np.array_equal(
        vec.vector, np.array([1.5, 2, 3])
    ), "Vector initialization failed"


def test_vector_dot_product(vector1, vector2):
    assert vector1 * vector2 == 32, f"Expected 32, got {vector1 * vector2}"


def test_vector_length(vector1):
    assert len(vector1) == 3, f"Expected length 3, got {len(vector1)}"


def test_vector_norm():
    v = Vector([3, 4])
    assert v.norm() == 5.0, f"Expected norm 5.0, got {v.norm()}"


def test_vector_angle():
    v1 = Vector([1, 0])
    v2 = Vector([0, 1])
    angle = v1 ^ v2
    assert np.isclose(angle, np.pi / 2), f"Expected angle π/2, got {angle}"


def test_zero_vector_norm():
    v = Vector([0, 0, 0])
    with pytest.raises(ZeroDivisionError):
        v ^ v  # This should raise ZeroDivisionError


# Matrix Tests
def test_matrix_initialization():
    m = Matrix([[1, 2], [3, 4]])
    assert np.array_equal(
        m.matrix, np.array([[1, 2], [3, 4]])
    ), "Matrix initialization failed"


def test_matrix_addition(matrix1, matrix2):
    result = matrix1 + matrix2
    expected = Matrix([[6, 8], [10, 12]])
    assert np.array_equal(result.matrix, expected.matrix), "Matrix addition failed"


def test_addition_with_zero_matrix():
    m1 = Matrix([[1, 2], [3, 4]])
    zero_matrix = Matrix([[0, 0], [0, 0]])
    result = m1 + zero_matrix
    assert np.array_equal(result.matrix, m1.matrix), "Adding zero matrix failed"


def test_matrix_multiplication(matrix1, matrix2):
    result = matrix1 @ matrix2
    expected = Matrix([[19, 22], [43, 50]])
    assert np.array_equal(
        result.matrix, expected.matrix
    ), "Matrix multiplication failed"


def test_identity_multiplication():
    m1 = Matrix([[1, 2], [3, 4]])
    identity = Matrix([[1, 0], [0, 1]])
    result = m1 @ identity
    assert np.array_equal(result.matrix, m1.matrix), "Identity multiplication failed"


def test_matrix_transpose():
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    result = m.T()
    expected = Matrix([[1, 4], [2, 5], [3, 6]])
    assert np.array_equal(result.matrix, expected.matrix), "Matrix transpose failed"


def test_matrix_addition_incompatible_sizes():
    m1 = Matrix([[1, 2]])
    m2 = Matrix([[1], [2]])
    with pytest.raises(ValueError):
        m1 + m2  # This should raise ValueError
