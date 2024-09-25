import numpy as np
from math import acos


class Vector:
    """
    A class for working with vectors.

    Attributes:
    ----------
    vector : numpy.ndarray
        An array representing the vector.

    Methods:
    -------
    __init__(data: list[float])
        Initializes a Vector object with the given data.

    __mul__(other: "Vector") -> float
        Returns the dot product of two vectors.

    __len__() -> int
        Returns the length of the vector.

    norm() -> float
        Returns the norm (length) of the vector.

    __xor__(other: "Vector") -> float
        Returns the angle between two vectors in radians.

    __repr__() -> str
        Returns a string representation of the vector.
    """

    def __init__(self, data: list[float]):
        """
        Initializes a Vector object.

        Parameters:
        ----------
        data : list[float]
            A list of values to create the vector.
        """
        self.vector = np.array(data)

    def __mul__(self, other: "Vector") -> float:
        """
        Computes the dot product of two vectors.

        Parameters:
        ----------
        other : Vector
            The vector to multiply with.

        Returns:
        -------
        float
            The dot product of the two vectors.

        Raises:
        ------
        ValueError
            If the lengths of the vectors are not the same.
        """
        if len(self) != len(other):
            raise ValueError("Vectors must have the same length.")
        return float(np.dot(self.vector, other.vector))

    def __len__(self) -> int:
        """
        Returns the length of the vector.

        Returns:
        -------
        int
            The number of elements in the vector.
        """
        return len(self.vector)

    def norm(self) -> float:
        """
        Computes the norm (length) of the vector.

        Returns:
        -------
        float
            The norm of the vector.
        """
        return float(np.linalg.norm(self.vector))

    def __xor__(self, other: "Vector") -> float:
        """
        Computes the angle between two vectors.

        Parameters:
        ----------
        other : Vector
            The vector to find the angle with.

        Returns:
        -------
        float
            The angle between the two vectors in radians.

        Raises:
        ------
        ValueError
            If the lengths of the vectors are not the same.
        ZeroDivisionError
            If the norm of one of the vectors is zero.
        """
        if len(self) != len(other):
            raise ValueError("Vectors must have the same length.")
        if (self.norm() * other.norm()) == 0:
            raise ZeroDivisionError("The norm of one of the vectors is zero.")
        return float(
            acos(np.dot(self.vector, other.vector) / (self.norm() * other.norm()))
        )

    def __repr__(self) -> str:
        """
        Returns a string representation of the vector.

        Returns:
        -------
        str
            A string representation of the vector.
        """
        return f"Vector({self.vector.tolist()})"


class Matrix:
    """
    A class for working with matrices.

    Attributes:
    ----------
    matrix : numpy.ndarray
        An array representing the matrix.

    Methods:
    -------
    __init__(data: list[list[float]])
        Initializes a Matrix object with the given data.

    __add__(other: "Matrix") -> "Matrix"
        Adds two matrices.

    __matmul__(other: "Matrix") -> "Matrix"
        Multiplies two matrices.

    T() -> "Matrix"
        Returns the transpose of the matrix.

    __repr__() -> str
        Returns a string representation of the matrix.
    """

    def __init__(self, data: list[list[float]]):
        """
        Initializes a Matrix object.

        Parameters:
        ----------
        data : list[list[float]]
            A 2D list to create the matrix.
        """
        self.matrix = np.array(data)

    def __add__(self, other: "Matrix") -> "Matrix":
        """
        Adds two matrices.

        Parameters:
        ----------
        other : Matrix
            The matrix to add.

        Returns:
        -------
        Matrix
            The result of the addition.

        Raises:
        ------
        ValueError
            If the shapes of the matrices are not the same.
        """
        if self.matrix.shape != other.matrix.shape:
            raise ValueError("Matrices must have the same shape for addition.")
        return Matrix((self.matrix + other.matrix).tolist())

    def __matmul__(self, other: "Matrix") -> "Matrix":
        """
        Multiplies two matrices.

        Parameters:
        ----------
        other : Matrix
            The matrix to multiply with.

        Returns:
        -------
        Matrix
            The result of the multiplication.

        Raises:
        ------
        ValueError
            If the matrices are not compatible for multiplication.
        """
        if self.matrix.shape[1] != other.matrix.shape[0]:
            raise ValueError("Matrices are not compatible for multiplication.")
        return Matrix(np.matmul(self.matrix, other.matrix).tolist())

    def T(self) -> "Matrix":
        """
        Returns the transpose of the matrix.

        Returns:
        -------
        Matrix
            The transposed matrix.
        """
        return Matrix(self.matrix.T.tolist())

    def __repr__(self) -> str:
        """
        Returns a string representation of the matrix.

        Returns:
        -------
        str
            A string representation of the matrix.
        """
        return f"Matrix({self.matrix.tolist()})"
