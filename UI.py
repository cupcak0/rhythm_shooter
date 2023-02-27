import pygame as pg
from Camera import *
from Renderer import *
import numpy as np
from numba import njit
from Functions import *
from Constant import *
from Enemy import *
from PointSystem import *
from Player import Player


def render(player: Player, surface: pg.surface.Surface):
    draw_compas(player, surface)
    draw_takt(player, surface)
    draw_score(player, surface)


def draw_compas(player: Player, surface: pg.surface.Surface):
    lines = []
    for enemy in player.enemy_system.enemies:
        direction = enemy.position - player.camera.forward_vector
        end_pos = (WIDTH / 2 - direction[0] * 100, HEIGHT / 2 - direction[1] * 100)
        lines.append(
            (
                direction[2],
                (
                    np.array([255, 255, 255])/(1+magnitude(direction)),
                    (WIDTH / 2, HEIGHT / 2),
                    end_pos,
                ),
            )
        )

    right = player.camera.right_vector
    mx_end_pos = (WIDTH / 2 - right[0] * 100, HEIGHT / 2 - right[1] * 100)
    x_end_pos = (WIDTH / 2 + right[0] * 100, HEIGHT / 2 + right[1] * 100)
    lines.append((right[2], ((255, 0, 0), (WIDTH / 2, HEIGHT / 2), x_end_pos)))
    lines.append((-right[2], ((127, 0, 0), (WIDTH / 2, HEIGHT / 2), mx_end_pos)))

    up = player.camera.up_vector
    y_end_pos = (WIDTH / 2 - up[0] * 100, HEIGHT / 2 - up[1] * 100)
    my_end_pos = (WIDTH / 2 + up[0] * 100, HEIGHT / 2 + up[1] * 100)
    lines.append((up[2], ((0, 255, 0), (WIDTH / 2, HEIGHT / 2), y_end_pos)))
    lines.append((-up[2], ((0, 127, 0), (WIDTH / 2, HEIGHT / 2), my_end_pos)))

    forward = player.camera.forward_vector
    mz_end_pos = (WIDTH / 2 - forward[0] * 100, HEIGHT / 2 - forward[1] * 100)
    z_end_pos = (WIDTH / 2 + forward[0] * 100, HEIGHT / 2 + forward[1] * 100)
    lines.append((forward[2], ((0, 0, 255), (WIDTH / 2, HEIGHT / 2), z_end_pos)))
    lines.append((-forward[2], ((0, 0, 127), (WIDTH / 2, HEIGHT / 2), mz_end_pos)))

    lines = sorted(lines)[::-1]
    for z, line in lines:
        pg.draw.line(surface, *line)


def draw_takt(player: Player, surface: pg.surface.Surface):
    height = HEIGHT / 8 * 7
    coeff = 100
    pg.draw.rect(surface, (127, 127, 127), (WIDTH / 2, height - 50, coeff, 100))

    pg.draw.line(
        surface,
        WHITE,
        (WIDTH / 2, height),
        (
            WIDTH / 2
            + (
                sum(player.point_system.track[player.point_system.track_pos :])
                - player.point_system.time
            )
            * coeff,
            height,
        ),
        3,
    )

    pos = (
        player.point_system.track[player.point_system.track_pos]
        - player.point_system.time
    )
    if not player.point_system.shot:
        pg.draw.line(
            surface,
            WHITE,
            (WIDTH / 2 + pos * coeff, height - 50),
            (WIDTH / 2 + pos * coeff, height + 50),
            1,
        )
    start = pos
    for beat in player.point_system.track[player.point_system.track_pos + 1 :]:
        beat_pos = beat + start
        pg.draw.line(
            surface,
            WHITE,
            (WIDTH / 2 + beat_pos * coeff, height - 50),
            (WIDTH / 2 + beat_pos * coeff, height + 50),
            1,
        )
        start += beat


def draw_score(player: Player, surface: pg.surface.Surface):
    text = FONT.render(
        "{} {}%".format(
            str(int(player.point_system.points * 10)),
            str(int(player.point_system.get_accuracy() * 100)),
        ),
        False,
        WHITE,
    )
    width = WIDTH / 16
    height = HEIGHT / 8 * 7
    surface.blit(text, (width, height - 75))
