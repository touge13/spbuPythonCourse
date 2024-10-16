from math import sqrt, acos


class Vector:
    """
    A class for working with vectors.

    Attributes:
    ----------
    vector : list[float]
        A list representing the vector.

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
        self.vector = data

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

        return sum(self.vector[i] * other.vector[i] for i in range(len(self)))

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
        return sqrt(sum(x**2 for x in self.vector))

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
        norm_self = self.norm()
        norm_other = other.norm()
        if norm_self == 0 or norm_other == 0:
            raise ZeroDivisionError("The norm of one of the vectors is zero.")

        dot_product = self * other
        return acos(dot_product / (norm_self * norm_other))

    def __repr__(self) -> str:
        """
        Returns a string representation of the vector.

        Returns:
        -------
        str
            A string representation of the vector.
        """
        return f"Vector({self.vector})"
