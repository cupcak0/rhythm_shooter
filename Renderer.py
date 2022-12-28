import math
import pygame as pg
import numpy as np
import pyquaternion as pq
FORWARD = np.array([0,0,1])
UP = np.array([0,1,0])
RIGHT = np.array([1,0,0])


class Renderer:
    def raymarch(ray_origin, ray_direction, distance_map):
        ret = np.array([0,0,0,0])

        MAXSTEP = 20
        MAXDIST = 10
        t = 0 # Расстояние, пройденное лучём
        for i in range(MAXSTEP):
            if t > MAXDIST:
                break
            p = ray_origin + ray_direction * t # Мировое положение луча
            dist = distance_map(p);       # Поле расстояний
            
            # Если поле меньше 0, то мы попали во что-то
            if dist < 0.01:
                ret = np.array([255, 255, 255, 1])
                break
            
            # Если не попали, то идём дальше
            t += dist
        
        return ret

    # Для каждого пикселя отправляет луч, и отрисовывает полученный цвет на экран
    def render(screen, cam, screen_size, distance_map):
        screen_width, screen_height = screen_size
        half_screen_width, half_screen_height = screen_width//2, screen_height//2

        STEP = 40
        for i in range(-half_screen_width, half_screen_width, STEP):
            for j in range(-half_screen_height, half_screen_height, STEP):
                # Поворот луча в градусах
                x_degrees = cam.fov * cam.aspect * i / screen_width
                y_degrees = cam.fov * j / screen_height

                # Поворот луча как кватернион
                y_angle = pq.Quaternion(axis=[1.0, 0.0, 0.0], degrees=y_degrees)
                x_angle = pq.Quaternion(axis=[0.0, 1.0, 0.0], degrees=x_degrees)
                angle = x_angle * y_angle

                # Вектор направления луча
                ray_direction = (cam.angle * angle).rotate(np.array([0, 0, 1]))

                ray = Renderer.raymarch(cam.position, ray_direction, distance_map)
                screen.fill(ray, (i + half_screen_width, j + half_screen_height, STEP, STEP))
