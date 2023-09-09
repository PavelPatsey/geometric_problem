import random
import matplotlib.pyplot as plt

MAX_TRIAL_COORDINATE_RANGE = 20
RANGE_COEFFICIENT = 1
MAX_POINTS_COORDINATE_RANGE = MAX_TRIAL_COORDINATE_RANGE * RANGE_COEFFICIENT
POINT_AMOUNT = 40


def get_segment_length(segment):
    ((x0, y0), (x1, y1)) = segment
    return ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5


def get_intersection_segment_of_segment_and_triangle(segment, triangle):
    triangle_segments = get_all_segments_from_points(triangle)

    intersection_points = (get_intersection_point(segment, triangle_segment) for triangle_segment in triangle_segments)
    intersection_points = filter(lambda x: x is not None, intersection_points)
    intersection_points = set(intersection_points)

    intersection_segment = (
        point if is_point_on_segment(point, segment) else None
        for point in intersection_points
        for segment in triangle_segments
    )
    intersection_segment = filter(lambda x: x is not None, intersection_segment)
    intersection_segment = tuple(set(intersection_segment))

    if len(intersection_segment) == 2:
        return intersection_segment


def get_all_segments_from_points(points):
    return [(points[i], points[j]) for i in range(len(points)) for j in range(i + 1, len(points))]


def get_random_point(coordinate_range):
    return tuple((random.uniform(-coordinate_range, coordinate_range) for _ in range(2)))


def get_random_triangle(coordinate_range):
    return tuple(get_random_point(coordinate_range) for _ in range(3))


def is_point_on_segment(point, segment):
    ((x0, y0), (x1, y1)) = segment
    (x, y) = point
    return (
        (x - x0) * (y1 - y0) == (y - y0) * (x1 - x0)
        and min(x0, x1) <= x <= max(x0, x1)
        and min(y0, y1) <= y <= max(y0, y1)
    )


def get_segment_coefficients(segment):
    ((x0, y0), (x1, y1)) = segment
    a = (y1 - y0) / (x1 - x0)
    b = y0 - a * x0
    return a, b


def get_intersection_point(segment_1, segment_2):
    ((x0, y0), (x1, y1)) = segment_1
    ((x2, y2), (x3, y3)) = segment_2

    # case when segment_1 or/and segment_2 is vertical
    if x0 == x1:
        if x2 == x3:
            return
        else:
            a, b = get_segment_coefficients(segment_2)
            x = x0
            y = a * x + b
            return x, y

    a, c = get_segment_coefficients(segment_1)
    b, d = get_segment_coefficients(segment_2)

    if a == b:  # if segments are parallel
        return
    x = (d - c) / (a - b)
    y = a * x + c
    return x, y


def main():
    points = [get_random_point(MAX_POINTS_COORDINATE_RANGE) for _ in range(POINT_AMOUNT)]
    triangle = get_random_triangle(MAX_TRIAL_COORDINATE_RANGE)
    segments = get_all_segments_from_points(points)
    intersection_segments = [
        get_intersection_segment_of_segment_and_triangle(segment, triangle) for segment in segments
    ]

    zipped = zip(segments, intersection_segments)
    zipped = filter(lambda x: x[1] is not None, zipped)
    zipped = map(lambda x: (x[0], x[1], get_segment_length(x[1])), zipped)
    if not zipped:
        print('No intersection segments')
        return
    max_segment = max(zipped, key=lambda x: x[2])
    print(f"point = {max_segment[0]}, segment = {max_segment[1]}, length = {max_segment[2]}")

    for point in points:
        plt.scatter(*point, color='blue')

    triangle_segments = get_all_segments_from_points(triangle)
    for segment in triangle_segments:
        ((x1, y1), (x2, y2)) = segment
        plt.plot([x1, x2], [y1, y2], color='green')

    ((x1, y1), (x2, y2)) = max_segment[0]
    plt.plot([x1, x2], [y1, y2], color='black')

    ((x1, y1), (x2, y2)) = max_segment[1]
    plt.plot([x1, x2], [y1, y2], color='red')

    plt.show()


if __name__ == "__main__":
    segment_1 = ((0, 0), (1, 1))
    segment_2 = ((-0.5, 1), (1.5, 0))
    p = get_intersection_point(segment_1, segment_2)
    assert p == (0.5, 0.5)

    segment_1 = ((0, 0), (0, 1))
    segment_2 = ((-1, 0), (0, 2))
    p = get_intersection_point(segment_1, segment_2)
    assert p == (0, 2)

    segment_1 = ((0, 0), (0, 1))
    segment_2 = ((-1, 0), (2, 0))
    p = get_intersection_point(segment_1, segment_2)
    assert p == (0, 0)

    segment_1 = ((0, 0), (0, 1))
    segment_2 = ((0, 2), (2, 0))
    p = get_intersection_point(segment_1, segment_2)
    assert p == (0, 2)

    segment_1 = ((0, 0), (1, 1))
    segment_2 = ((1, 1), (2, 2))
    p = get_intersection_point(segment_1, segment_2)
    assert p is None

    segment_1 = ((0, 0), (1, 1))
    segment_2 = ((1, 0), (2, 1))
    p = get_intersection_point(segment_1, segment_2)
    assert p is None

    segment_1 = ((0, 0), (1, 1))
    segment_2 = ((0, 0), (1, 1))
    p = get_intersection_point(segment_1, segment_2)
    assert p is None

    assert is_point_on_segment((0.5, 0.5), ((0, 0), (1, 1))) is True
    assert is_point_on_segment((0.5, 0.5), ((0, 1), (1, 1))) is False
    assert is_point_on_segment((-2, -2), ((-1, 0), (-0.5, 1))) is False

    segment = ((0, 0), (0, 1))
    triangle = ((-1, -0), (0, 2), (2, 0))
    intersection_segment = get_intersection_segment_of_segment_and_triangle(segment, triangle)
    assert set(intersection_segment) == set(((0, 0), (0, 2)))

    segment = ((0, 0), (1, 1))
    triangle = ((-1, -0), (-0.5, 1), (1.5, 0))
    intersection_segment = get_intersection_segment_of_segment_and_triangle(segment, triangle)
    assert set(intersection_segment) == set(((0, 0), (0.5, 0.5)))

    segment = ((-2, 0), (0, 2))
    triangle = ((-1, -0), (-0.5, 1), (1.5, 0))
    intersection_segment = get_intersection_segment_of_segment_and_triangle(segment, triangle)
    assert intersection_segment is None

    main()
