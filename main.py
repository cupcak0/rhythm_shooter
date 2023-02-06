import pygame as pg
import Camera
from Renderer import render
import numpy as np
from numba import njit
from Functions import *
from Constant import *

@njit(fastmath=True, cache=True)
def distance_map(pos):
    return distance_sphere_tardis(pos, 0.5)

if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('Raymarching')
    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN | pg.DOUBLEBUF)
    pg.event.set_allowed([pg.QUIT, pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, pg.MOUSEMOTION, pg.KEYDOWN])
    screen.set_alpha(None)
    clock = pg.time.Clock()
    fov = 30
    aspect = WIDTH/HEIGHT
    cam = Camera.Camera(position=np.array([0,1,0]), aspect=aspect, fov=fov)
    running = True
    right_pressed = False

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 3:
                    right_pressed = True
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 3:
                    right_pressed = False
            elif event.type == pg.MOUSEMOTION:
                if right_pressed:
                    x, y = event.rel
                    cam.rotate(x,-y)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    cam.move(np.array([0,0,1]))
                elif event.key == pg.K_s:
                    cam.move(np.array([0,0,-1]))
                elif event.key == pg.K_d:
                    cam.move(np.array([-1,0,0]))
                elif event.key == pg.K_a:
                    cam.move(np.array([1,0,0]))

        render(screen, cam,(WIDTH,HEIGHT),distance_map)
        pg.display.flip()
        clock.tick(FPS)
    pg.quit()