def get_rgba_element(i):
    rgba_generator = (
        (r, g, b, a)
        for r in range(256)
        for g in range(256)
        for b in range(256)
        for a in range(0, 101, 2)
    )
    for idx, rgba in enumerate(rgba_generator):
        if idx == i:
            return rgba
