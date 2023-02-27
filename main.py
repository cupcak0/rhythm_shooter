import pygame as pg
import numpy as np
from pygame_widgets.button import Button
import pygame_widgets as pw
from numba import njit
import math
from Camera import Camera
from Renderer import render
from Functions import *
from Constant import *
from Enemy import *
from Player import *
import UI
import scipy


@njit(fastmath=True, cache=True)
def distance_map(pos, enemies):
    mn = MAXDIST
    for enemy in enemies:
        mn = min(mn, distance_octahedron(pos, enemy, 0.1))
    return mn


def enemies_distance_map(pos, enemies):
    mn = MAXDIST
    ans = None
    for enemy in enemies:
        if distance_octahedron(pos, enemy.position, 0.1) <= mn:
            mn = min(mn, distance_octahedron(pos, enemy.position, 0.1))
            ans = enemy
    return (mn, ans)


def play_screen():
    exit_button.hide()
    play_button.hide()
    b.hide()
    pg.mouse.set_visible(False)
    fov = 30
    aspect = WIDTH / HEIGHT
    cam = Camera(aspect=aspect, fov=fov)
    enemy_system = EnemySystem(3)
    player = Player(cam, enemy_system)
    running = True
    render(screen, player, (WIDTH, HEIGHT), distance_map)
    UI.render(player, screen)
    pg.display.flip()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.shoot_enemy(enemies_distance_map)
            elif event.type == pg.MOUSEMOTION:
                x, y = event.rel
                player.camera.rotate(x, -y / aspect)

        enemy_system.update()
        render(screen, player, (WIDTH, HEIGHT), distance_map)
        UI.render(player, screen)
        pg.display.flip()
        time = clock.tick(FPS)
        if not player.point_system.update(time / 1000):
            running = False
    end_screen(
        int(player.point_system.points * 10),
        int(player.point_system.get_accuracy() * 100),
    )


def end_screen(points, accuracy):
    b.show()
    screen.fill((0, 0, 0))
    pg.mouse.set_visible(True)

    running = True

    while running:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
        screen.fill((0, 0, 0))
        text = MENU_FONT.render(
            "Очки: {}, Точность: {}%".format(points, accuracy), False, WHITE
        )
        screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 8))
        if b.clicked:
            running = False
        pw.update(events)
        pg.display.flip()


def menu_screen():
    screen.fill((0, 0, 0))
    pg.mouse.set_visible(True)

    running = True

    text = FONT.render("Такт", False, WHITE)

    while running:
        exit_button.show()
        play_button.show()
        b.hide()
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
        if exit_button.clicked:
            running = False
        screen.fill((0, 0, 0))
        screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 8))
        pw.update(events)
        pg.display.flip()


if __name__ == "__main__":
    pg.init()
    pg.display.set_caption("Takt")
    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN | pg.DOUBLEBUF)
    WIDTH, HEIGHT = pg.display.get_window_size()
    pg.event.set_allowed(
        [pg.QUIT, pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, pg.MOUSEMOTION, pg.KEYDOWN]
    )
    screen.set_alpha(None)
    clock = pg.time.Clock()
    exit_button = Button(
        screen,
        WIDTH / 8 * 3,
        HEIGHT / 8 * 6,
        WIDTH / 8 * 2,
        HEIGHT / 8,
        text="Выход",
        font=MENU_FONT,
        inactiveColour=(127, 127, 127),
        hoverColour=(255, 255, 255),
    )

    play_button = Button(
        screen,
        WIDTH / 8 * 3,
        HEIGHT / 8 * 4,
        WIDTH / 8 * 2,
        HEIGHT / 8,
        onClick=play_screen,
        text="Играть",
        font=MENU_FONT,
        inactiveColour=(127, 127, 127),
        hoverColour=(255, 255, 255),
    )
    b = Button(
        screen,
        WIDTH / 8 * 3,
        HEIGHT / 8 * 6,
        WIDTH / 8 * 2,
        HEIGHT / 8,
        text="Главное меню",
        font=MENU_FONT,
        inactiveColour=(127, 127, 127),
        hoverColour=(255, 255, 255),
    )
    exit_button.hide()
    play_button.hide()
    b.hide()
    menu_screen()
    pg.quit()
