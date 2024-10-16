class Matrix:
    """
    A class for working with matrices.

    Attributes:
    ----------
    matrix : list[list[float]]
        A 2D list representing the matrix.

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
        self.matrix = data

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
        if len(self.matrix) != len(other.matrix) or len(self.matrix[0]) != len(
            other.matrix[0]
        ):
            raise ValueError("Matrices must have the same shape for addition.")

        result = [
            [self.matrix[i][j] + other.matrix[i][j] for j in range(len(self.matrix[0]))]
            for i in range(len(self.matrix))
        ]
        return Matrix(result)

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
        if len(self.matrix[0]) != len(other.matrix):
            raise ValueError("Matrices are not compatible for multiplication.")

        result = [
            [
                sum(
                    self.matrix[i][k] * other.matrix[k][j]
                    for k in range(len(other.matrix))
                )
                for j in range(len(other.matrix[0]))
            ]
            for i in range(len(self.matrix))
        ]
        return Matrix(result)

    def T(self) -> "Matrix":
        """
        Returns the transpose of the matrix.

        Returns:
        -------
        Matrix
            The transposed matrix.
        """
        result = [
            [self.matrix[j][i] for j in range(len(self.matrix))]
            for i in range(len(self.matrix[0]))
        ]
        return Matrix(result)

    def __repr__(self) -> str:
        """
        Returns a string representation of the matrix.

        Returns:
        -------
        str
            A string representation of the matrix.
        """
        return f"Matrix({self.matrix})"
