import pytest
import numpy as np
from project.matrix_operations import Matrix

# Fixtures
@pytest.fixture
def matrix1():
    return Matrix([[1.5, 2], [3, 4]])


@pytest.fixture
def matrix2():
    return Matrix([[5, 6], [7, 8]])


# Matrix Tests
def test_matrix_initialization():
    m = Matrix([[1.5, 2], [3, 4]])
    assert np.array_equal(
        m.matrix, np.array([[1.5, 2], [3, 4]])
    ), "Matrix initialization failed"


def test_matrix_addition(matrix1, matrix2):
    result = matrix1 + matrix2
    expected = Matrix([[6.5, 8], [10, 12]])
    assert np.array_equal(result.matrix, expected.matrix), "Matrix addition failed"


def test_addition_with_zero_matrix():
    m1 = Matrix([[1.5, 2], [3, 4]])
    zero_matrix = Matrix([[0, 0], [0, 0]])
    result = m1 + zero_matrix
    assert np.array_equal(result.matrix, m1.matrix), "Adding zero matrix failed"


def test_matrix_multiplication(matrix1, matrix2):
    result = matrix1 @ matrix2
    expected = Matrix([[21.5, 25], [43, 50]])
    assert np.array_equal(
        result.matrix, expected.matrix
    ), "Matrix multiplication failed"


def test_identity_multiplication():
    m1 = Matrix([[1.5, 2], [3, 4]])
    identity = Matrix([[1, 0], [0, 1]])
    result = m1 @ identity
    assert np.array_equal(result.matrix, m1.matrix), "Identity multiplication failed"


def test_matrix_transpose():
    m = Matrix([[1.5, 2, 3], [4, 5, 6]])
    result = m.T()
    expected = Matrix([[1.5, 4], [2, 5], [3, 6]])
    assert np.array_equal(result.matrix, expected.matrix), "Matrix transpose failed"


def test_matrix_addition_incompatible_sizes():
    m1 = Matrix([[1.5, 2]])
    m2 = Matrix([[1], [2]])
    with pytest.raises(ValueError):
        m1 + m2  # This should raise ValueError
