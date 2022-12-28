import pygame
import Camera
from Renderer import Renderer
import numpy as np

WIDTH = 1920
HEIGHT = 1080

def distance_sphere(p, sphere_pos, d):
    return np.linalg.norm(p - sphere_pos) - d

def distance_torus(p, t):
    q = np.array([np.linalg.norm(np.array([p[0],p[2]])) - t[0], p[1]])
    return np.linalg.norm(q) - t[1]

def distance_map(pos):
    return min(distance_torus(pos, np.array([0.5,0.1])), distance_torus(pos, np.array([2,0.1])))

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Raymarching')
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN + pygame.DOUBLEBUF + pygame.HWSURFACE)
    fps = 60
    clock = pygame.time.Clock()
    cam = Camera.Camera(position=np.array([1,1,0]), aspect=WIDTH/HEIGHT, fov=90)

    running = True
    right_pressed = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    right_pressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    right_pressed = False
            if event.type == pygame.MOUSEMOTION:
                if right_pressed:
                    x, y = event.rel
                    cam.rotate(x,y)

        Renderer.render(screen, cam, (WIDTH,HEIGHT), distance_map)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()