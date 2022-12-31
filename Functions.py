import numpy as np
from numba import njit
import math

@njit(fastmath=True)
def magnitude(a):
    ans = 0
    for i in range(len(a)):
        ans += a[i]*a[i]
    return ans**0.5

@njit(fastmath=True)
def distance_sphere(p, sphere_pos, d):
    return magnitude(p - sphere_pos) - d

@njit(fastmath=True)
def distance_sphere_tardis(p, sphere_pos, d):
    return magnitude(np.array([(p[0]+2)%4-2,(p[1]+2)%4-2,(p[2]+2)%4-2]) - sphere_pos) - d
    
@njit(fastmath=True)
def distance_torus(p, t):
    q = np.array([magnitude(np.array([p[0],p[2]])) - t[0], p[1]])
    return magnitude(q) - t[1]

# Вращает вектор с помощью матрицы вращения
# Принимает как вращение либо углы в градусы либо синусы и косинусы углов
def rotate(v, *args):
    if len(args) == 4:
        sin_y, cos_y, sin_x, cos_x = args
        matrix_x = np.array([np.array([1.0,0.0,0.0]), np.array([0.0,cos_x,-sin_x]), np.array([0.0, sin_x, cos_x])])
        matrix_y = np.array([np.array([cos_y,0.0,sin_y]), np.array([0.0,1.0,0.0]), np.array([-sin_y,0.0, cos_y])])
        return matrix_x.dot(matrix_y).dot(v)
    elif len(args) == 2:
        degrees_x, degrees_y = args
        a = math.radians(degrees_y)
        sin_a, cos_a = math.sin(a), math.cos(a)
        matrix_x = np.array([np.array([1.0,0.0,0.0]), np.array([0.0,cos_a,-sin_a]), np.array([0.0, sin_a, cos_a])])
        b = math.radians(degrees_x)
        sin_b, cos_b = math.sin(b), math.cos(b)
        matrix_y = np.array([np.array([cos_b,0.0,sin_b]), np.array([0.0,1.0,0.0]), np.array([-sin_b,0.0, cos_b])])
        return matrix_x.dot(matrix_y).dot(v)

@njit(fastmath=True)
def normalize(a):
    return a / np.max(np.abs(a))

@njit(fastmath=True)
def calc_normal(pos, distance_map):
    EPS = np.array([0.01, 0.0])
    XYY = np.array([EPS[0],EPS[1],EPS[1]])
    YXY = np.array([EPS[1], EPS[0], EPS[1]])
    YYX = np.array([EPS[1],EPS[1],EPS[0]])
    nor = np.array([
        distance_map(pos + XYY) - distance_map(pos - XYY),
        distance_map(pos + YXY) - distance_map(pos - YXY),
        distance_map(pos + YYX) - distance_map(pos - YYX)])
    return normalize(nor)