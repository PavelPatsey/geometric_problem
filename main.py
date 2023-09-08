import random

import pytest

MAX_TRIAL_COORDINATE_RANGE = 10
RANGE_COEFFICIENT = 10
MAX_POINTS_COORDINATE_RANGE = MAX_TRIAL_COORDINATE_RANGE * RANGE_COEFFICIENT
POINT_AMOUNT = 10


def get_all_vectors_from_points(points):
    return [(points[i], points[j]) for i in range(len(points)) for j in range(i + 1, len(points))]


def get_random_point(coordinate_range):
    return tuple((random.uniform(-coordinate_range, coordinate_range) for _ in range(2)))


def get_random_triangle(coordinate_range):
    return tuple(get_random_point(coordinate_range) for _ in range(3))


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
        raise ValueError("Vectors are parallel")
    else:
        x = (d - c) / (a - b)
        y = a * x + c
        return x, y


def main():
    print("start main")
    points = [get_random_point(MAX_POINTS_COORDINATE_RANGE) for _ in range(POINT_AMOUNT)]
    print(f"{points=}")
    triangle = get_random_triangle(MAX_TRIAL_COORDINATE_RANGE)
    print(f"{triangle=}")
    vectors = get_all_vectors_from_points(points)
    print(f"{vectors=}")


if __name__ == "__main__":
    vector_1 = ((0, 0), (1, 1))
    vector_2 = ((-0.5, 1), (1.5, 0))
    p = get_intersection_point(vector_1, vector_2)
    assert p == (0.5, 0.5)

    with pytest.raises(ValueError) as err_info:
        vector_1 = ((0, 0), (1, 1))
        vector_2 = ((1, 1), (2, 2))
        get_intersection_point(vector_1, vector_2)
    assert "Vectors are parallel" in str(err_info.value)

    assert is_point_on_segment((0.5, 0.5), ((0, 0), (1, 1))) is True
    assert is_point_on_segment((0.5, 0.5), ((0, 1), (1, 1))) is False

    main()
