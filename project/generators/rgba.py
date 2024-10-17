def rgba_generator():
    """
    Generator expression for producing a four-dimensional RGBA vector set.

    This generator creates all possible combinations of RGBA color values where:
        - Red (R), Green (G), and Blue (B) values range from 0 to 255.
        - Alpha (A), representing transparency, ranges from 0 to 100 but only includes even values.

    Yields:
        tuple: A tuple representing the (R, G, B, A) values.
    """
    return (
        (r, g, b, a)
        for r in range(256)
        for g in range(256)
        for b in range(256)
        for a in range(0, 101, 2)
    )


def get_rgba_element(i):
    """
    Function to retrieve the i-th RGBA element from the generator.

    Args:
        i (int): The index of the desired RGBA element.

    Returns:
        tuple: The (R, G, B, A) values at the i-th position in the generator.
    """
    for idx, rgba in enumerate(rgba_generator()):
        if idx == i:
            return rgba
