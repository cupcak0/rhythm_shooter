import math
import pygame as pg
import numpy as np
from numba import njit
import time
from Functions import *
FORWARD = np.array([0.0,0.0,1.0])
UP = np.array([0.0,1.0,0.0])
RIGHT = np.array([1.0,0.0,0.0])
STEP = 30
LIGHT_DIR = np.array([-0.5,0.5,0])


class Renderer:
    def raymarch(ray_origin, ray_direction, distance_map):
        ret = np.array([50,50,50]) if ray_direction[1] < 0 else np.array([100,100,100])

        MAXSTEP = 32
        MAXDIST = 20
        step = 0
        t = 0 # Расстояние, пройденное лучём
        for i in range(MAXSTEP):
            if t > MAXDIST:
                break
            step += 1
            p = ray_origin + ray_direction*t # Мировое положение луча
            dist = distance_map(p);       # Поле расстояний
            # Если поле меньше 0, то мы попали во что-то
            if dist < 0.01:
                ret = np.array([255, 255, 255]) * max(0, np.dot(calc_normal(p, distance_map),LIGHT_DIR))
                break
            
            # Если не попали, то идём дальше
            t += dist
            
        return ret

    def render(screen, cam, screen_size, distance_map):
        res = Renderer.render_cycle(cam.fov, cam.position, (cam.x_degrees, cam.y_degrees), screen_size, distance_map)
        for color, x, y in res:
                screen.fill(color, (x,y,STEP,STEP))
        
    # Для каждого пикселя отправляет луч, и отрисовывает полученный цвет на экран
    def render_cycle(fov, pos, cam_angle, screen_size, distance_map):
        res = []
        screen_width, screen_height = screen_size
        half_screen_width, half_screen_height = screen_width//2, screen_height//2
        coeff = fov/screen_height
        for i in range(-half_screen_width, half_screen_width, STEP):
            # Поворот луча по горизонтали
            x_degrees = coeff * i + cam_angle[0]
            x_radians = math.radians(x_degrees)
            sin_x, cos_x = math.sin(x_radians), math.cos(x_radians) 
            for j in range(-half_screen_height, half_screen_height, STEP):
                # Поворот луча по вертикали
                y_degrees = coeff * j + cam_angle[1]
                y_radians = math.radians(y_degrees)
                sin_y, cos_y = math.sin(y_radians), math.cos(y_radians) 
                # Вектор направления луча
                ray_direction = normalize(rotate(FORWARD, sin_x, cos_x, sin_y, cos_y))

                ray = Renderer.raymarch(pos, ray_direction, distance_map)
                res.append((ray, i + half_screen_width, j + half_screen_height))
        return res
