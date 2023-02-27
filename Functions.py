import numpy as np
from numba import njit, prange
import math

# Длина вектора
@njit(fastmath=True, cache=True)
def magnitude(a):
    ans = 0
    for i in prange(len(a)):
        ans += a[i] * a[i]
    return ans ** 0.5


@njit(fastmath=True, cache=True)
def distance_sphere(p, sphere_pos, d):
    return magnitude(sphere_pos - p) - d


@njit(fastmath=True, cache=True)
def distance_sphere_tardis(p, d):
    return (
        magnitude(
            np.array([(p[0] + 2) % 4 - 2, (p[1] + 2) % 4 - 2, (p[2] + 2) % 4 - 2])
        )
        - d
    )


@njit(fastmath=True, cache=True)
def distance_torus(p, t):
    q = np.array([magnitude(np.array([p[0], p[2]])) - t[0], p[1]])
    return magnitude(q) - t[1]


@njit(fastmath=True, cache=True)
def multiply_3x1_3x3(a0, b0, b1, b2):
    return np.array(
        [
            a0[0] * b0[0] + a0[1] * b1[0] + a0[2] * b2[0],
            a0[0] * b0[1] + a0[1] * b1[1] + a0[2] * b2[1],
            a0[0] * b0[2] + a0[1] * b1[2] + a0[2] * b2[2],
        ]
    )

@njit(fastmath=True, cache=True)
def degrotate(v, x, y):
    sin_x, cos_x = math.sin(math.radians(x)), math.cos(math.radians(x))
    sin_y, cos_y = math.sin(math.radians(y)), math.cos(math.radians(y))
    return rotate(v, sin_x, cos_x, sin_y, cos_y)


# Вращает вектор с помощью матрицы вращения
# Принимает как вращение синусы и косинусы углов
@njit(fastmath=True, cache=True)
def rotate(v, sin_y, cos_y, sin_x, cos_x):
    a = multiply_3x1_3x3(
        v,
        np.array([1.0, 0.0, 0.0]),
        np.array([0.0, cos_x, -sin_x]),
        np.array([0.0, sin_x, cos_x]),
    )
    b = multiply_3x1_3x3(
        a,
        np.array([cos_y, 0.0, sin_y]),
        np.array([0.0, 1.0, 0.0]),
        np.array([-sin_y, 0.0, cos_y]),
    )
    return b


@njit(fastmath=True, cache=True)
def normalize(a):
    return a / magnitude(a)


@njit(fastmath=True, cache=True)
def calc_normal(pos, distance_map, enemies):
    EPS = np.array([0.01, 0.0])
    XYY = np.array([EPS[0], EPS[1], EPS[1]])
    YXY = np.array([EPS[1], EPS[0], EPS[1]])
    YYX = np.array([EPS[1], EPS[1], EPS[0]])
    nor = np.array(
        [
            distance_map(pos + XYY, enemies) - distance_map(pos - XYY, enemies),
            distance_map(pos + YXY, enemies) - distance_map(pos - YXY, enemies),
            distance_map(pos + YYX, enemies) - distance_map(pos - YYX, enemies),
        ]
    )
    return normalize(nor)

@njit(fastmath=True, cache=True)
def distance_octahedron(p, op, s):
    p = p-op
    p = np.abs(p)
    return (p[0]+p[1]+p[2]-s)*0.57735027
