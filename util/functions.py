from math import sin, cos, radians

from util.vectors import Vector2


def rotate_around(origin: Vector2, point: Vector2, angle: float):
    x = origin.x + cos(radians(angle)) * (point.x - origin.x) - sin(radians(angle)) * (point.y - origin.y)
    y = origin.y + sin(radians(angle)) * (point.x - origin.x) + cos(radians(angle)) * (point.y - origin.y)
    return x, y


def unpack_vector_list(vector_list):  # seems to work
    if type(vector_list) is not list and type(vector_list) is not tuple:
        raise Exception(f'cannot unpack {type(vector_list)}')

    unpacked_list = []
    for vector in vector_list:
        unpacked_list.append(vector.components())
    return unpacked_list
