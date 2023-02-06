import math
import pygame as pg
import numpy as np
from numba import njit
from Functions import *
from Constant import *


@njit(fastmath=True, cache=True)
def raymarch(ray_origin, ray_direction, distance_map):
    ret = np.abs(normalize(ray_direction)) * 255

    MAXSTEP = 64
    MAXDIST = 64
    t = 0 # Расстояние, пройденное лучём
    for i in range(MAXSTEP):
        if t > MAXDIST:
            break
        p = ray_origin + ray_direction*t # Мировое положение луча
        dist = distance_map(p);       # Поле расстояний

        # Если поле меньше 0, то мы попали во что-то
        if dist < 0.01:
            ret = WHITE * max(0.0, np.dot(calc_normal(p, distance_map),LIGHT_DIR))
            break
            
        # Если не попали, то идём дальше
        t += dist
    return ret

def render(screen, cam, screen_size, distance_map):
    res = render_cycle(cam.fov, cam.position, (cam.x_degrees, cam.y_degrees), screen_size, distance_map)

    for color, x, y in res:
        screen.fill(color, (x,y,STEP,STEP))
        
# Для каждого пикселя отправляет луч, и отрисовывает полученный цвет на экран
@njit(fastmath=True, cache=True)
def render_cycle(fov, pos, cam_angle, screen_size, distance_map):
    res = []
    screen_width, screen_height = screen_size

    coeff = fov/screen_height
    
    screen_width, screen_height = screen_width//STEP, screen_height//STEP

    for i in range(0, screen_width):
        ii = i * STEP
        # Поворот луча по горизонтали
        x_degrees = coeff * ii + cam_angle[0]
        x_radians = math.radians(x_degrees)
        sin_x, cos_x = math.sin(x_radians), math.cos(x_radians) 

        for j in range(0, screen_height):
            jj = j * STEP
            # Поворот луча по вертикали
            y_degrees = coeff * jj + cam_angle[1]
            y_radians = math.radians(y_degrees)
            sin_y, cos_y = math.sin(y_radians), math.cos(y_radians) 

            # Вектор направления луча
            ray_direction = rotate(FORWARD, sin_x, cos_x, sin_y, cos_y)

            # Реймарчинг
            ray = raymarch(pos, ray_direction, distance_map)

            res.append((ray, ii, (screen_height*STEP)-jj))

    return res
