import pygame as pg
import Camera
from Renderer import Renderer
import numpy as np
from numba import njit
from Functions import *
WIDTH = 1920
HEIGHT = 1080

@njit(fastmath=True)
def distance_map(pos):
    return min(distance_torus(pos, (1, 0.2)), distance_torus(pos, (2, 0.2)))

if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('Raymarching')
    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN | pg.DOUBLEBUF)
    pg.event.set_allowed([pg.QUIT, pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, pg.MOUSEMOTION, pg.KEYDOWN])
    screen.set_alpha(None)
    fps = 30
    clock = pg.time.Clock()
    cam = Camera.Camera(position=np.array([0,2,-2]), aspect=WIDTH/HEIGHT, fov=90, y_degrees=45)
    running = True
    right_pressed = False
    Renderer.render(screen, cam,(WIDTH,HEIGHT),distance_map)
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
                    cam.rotate(x,y)
                    Renderer.render(screen, cam,(WIDTH,HEIGHT),distance_map)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    cam.move(np.array([0,0,1]))
                    Renderer.render(screen, cam,(WIDTH,HEIGHT),distance_map)
                elif event.key == pg.K_s:
                    cam.move(np.array([0,0,-1]))
                    Renderer.render(screen, cam,(WIDTH,HEIGHT),distance_map)
                elif event.key == pg.K_d:
                    cam.move(np.array([1,0,0]))
                    Renderer.render(screen, cam,(WIDTH,HEIGHT),distance_map)
                elif event.key == pg.K_a:
                    cam.move(np.array([-1,0,0]))
                    Renderer.render(screen, cam,(WIDTH,HEIGHT),distance_map)
                    
        pg.display.flip()
        clock.tick(fps)
    pg.quit()