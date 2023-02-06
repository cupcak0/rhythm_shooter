import numpy as np
from numba import njit, prange
import math

# Длина вектора
@njit(fastmath=True, cache=True)
def magnitude(a):
    ans = 0
    for i in prange(len(a)):
        ans += a[i]*a[i]
    return ans**0.5

@njit(fastmath=True, cache=True)
def distance_sphere(p, sphere_pos, d):
    return magnitude(p - sphere_pos) - d

@njit(fastmath=True, cache=True)
def distance_sphere_tardis(p, d):
    return magnitude(np.array([(p[0]+2)%4-2,(p[1]+2)%4-2,(p[2]+2)%4-2])) - d
    
@njit(fastmath=True, cache=True)
def distance_torus(p, t):
    q = np.array([magnitude(np.array([p[0],p[2]])) - t[0], p[1]])
    return magnitude(q) - t[1]

@njit(fastmath=True, cache=True)
def sinus(p):
    return p[1] - (math.sin(math.radians(p[0])) * math.sin(math.radians(p[2])))*4

@njit(fastmath=True, cache=True)
def multiply_3x1_3x3(a0,b0,b1,b2):
    return np.array([a0[0]*b0[0]+a0[1]*b1[0]+a0[2]*b2[0], a0[0]*b0[1]+a0[1]*b1[1]+a0[2]*b2[1], a0[0]*b0[2]+a0[1]*b1[2]+a0[2]*b2[2]])

# Вращает вектор с помощью матрицы вращения
# Принимает как вращение либо углы в градусы либо синусы и косинусы углов
@njit(fastmath=True, cache=True)
def rotate(v, *args):
    sin_y, cos_y, sin_x, cos_x = args
    a = multiply_3x1_3x3(v, np.array([1.0,0.0,0.0]), np.array([0.0,cos_x,-sin_x]), np.array([0.0, sin_x, cos_x]))
    b = multiply_3x1_3x3(a, np.array([cos_y,0.0,sin_y]), np.array([0.0,1.0,0.0]), np.array([-sin_y,0.0, cos_y]))
    return b

@njit(fastmath=True, cache=True)
def normalize(a):
    return a / np.max(np.abs(a))

@njit(fastmath=True, cache=True)
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