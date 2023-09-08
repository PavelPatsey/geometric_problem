def is_point_on_segment(point, vector):
    ((x0, y0), (x1, y1)) = vector
    (x, y) = point
    return (x - x0) * (y1 - y0) == (y - y0) * (x1 - x0)


def get_segment_equation_coefficients(vector):
    ((x0, y0), (x1, y1)) = vector
    a = (y1 - y0) / (x1 - x0)
    b = y0 - a * x0
    return a, b


def get_intersection_point(vector_1, vector_2):
    a, c = get_segment_equation_coefficients(vector_1)
    b, d = get_segment_equation_coefficients(vector_2)
    if a == b:
        return
    else:
        x = (d - c) / (a - b)
        y = a * x + c
        return x, y


def main():
    pass


if __name__ == "__main__":
    vector_1 = ((0, 0), (1, 1))
    vector_2 = ((-0.5, 1), (1.5, 0))
    p = get_intersection_point(vector_1, vector_2)
    assert p == (0.5, 0.5)

    vector_1 = ((0, 0), (1, 1))
    vector_2 = ((1, 1), (2, 2))
    p = get_intersection_point(vector_1, vector_2)
    assert p is None

    assert is_point_on_segment((0.5, 0.5), ((0, 0), (1, 1))) is True
    assert is_point_on_segment((0.5, 0.5), ((0, 1), (1, 1))) is False

    main()
