import math
import pygame as pg
import numpy as np
from numba import njit
from Functions import *
from Constant import *


@njit(fastmath=True, cache=True)
def raymarch(ray_origin, ray_direction, distance_map, enemies):
    ret = WHITE/2 * abs(math.sin(math.radians(ray_direction[0]*20)))

    t = 0  # Расстояние, пройденное лучём
    for i in range(MAXSTEP):
        if t > MAXDIST:
            break
        p = ray_origin + ray_direction * t  # Мировое положение луча
        dist = distance_map(p, enemies)
        # Поле расстояний

        # Если поле меньше 0, то мы попали во что-то
        if dist < 0.01:
            ret = WHITE * max(
                0.1, calc_normal(p, distance_map, enemies)@LIGHT_DIR
            )
            break

        # Если не попали, то идём дальше
        t += dist
    return ret


def enemy_raymarch(ray_origin, ray_direction, distance_map, enemies):
    ret = None

    t = 0  # Расстояние, пройденное лучём
    for i in range(MAXSTEP):
        if t > MAXDIST:
            break
        p = ray_origin + ray_direction * t  # Мировое положение луча
        dist, enemy = distance_map(p, enemies)
        # Поле расстояний

        # Если поле меньше 0, то мы попали во что-то
        if dist < 0.01:
            ret = enemy
            break

        # Если не попали, то идём дальше
        t += dist
    return ret


def render(screen, player, screen_size, distance_map):
    res = render_cycle(
        player.camera.fov,
        player.pos,
        (player.camera.x_degrees, player.camera.y_degrees),
        screen_size,
        distance_map,
        player.enemy_system.enemies_positions,
    )

    for color, x, y in res:
        screen.fill(color, (x, y, STEP, STEP))


# Для каждого пикселя отправляет луч, и отрисовывает полученный цвет на экран
@njit(fastmath=True, cache=True)
def render_cycle(fov, pos, cam_angle, screen_size, distance_map, enemies):
    res = []
    screen_width, screen_height = screen_size

    coeff = fov / screen_height

    screen_width, screen_height = screen_width // STEP, screen_height // STEP

    for i in range(0, screen_width):
        ii = i * STEP
        # Поворот луча по горизонтали
        x_degrees = coeff * ii + cam_angle[0]
        x_radians = math.radians(x_degrees)
        sin_x, cos_x = math.sin(x_radians), math.cos(x_radians)

        for j in range(1, screen_height + 1):
            jj = j * STEP
            # Поворот луча по вертикали
            y_degrees = coeff * jj + cam_angle[1]
            y_radians = math.radians(y_degrees)
            sin_y, cos_y = math.sin(y_radians), math.cos(y_radians)

            # Вектор направления луча
            ray_direction = rotate(FORWARD, sin_x, cos_x, sin_y, cos_y)

            # Реймарчинг
            ray = raymarch(pos, ray_direction, distance_map, enemies)
            res.append((ray, ii, (screen_height * STEP) - jj))

    return res
