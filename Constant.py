import numpy as np
import pygame as pg
import pygame_widgets as pw
from Functions import *

FORWARD = np.array([0.0, 0.0, 1.0])
UP = np.array([0.0, 1.0, 0.0])
RIGHT = np.array([1.0, 0.0, 0.0])
STEP = 15
LIGHT_DIR = normalize(np.array([-0.5, 1, 0]))
WHITE = np.array([255.0, 255.0, 255.0])
WIDTH = 1920
HEIGHT = 1080
FPS = 30
MAXSTEP = 64
MAXDIST = 64
pg.font.init()
FONT = pg.font.SysFont("Times New Roman", 100)
MENU_FONT = pg.font.SysFont("Times New Roman", 40)
TRACK = [10, 5, 5, 10, 5, 5, 10, 5, 5, 10, 3, 3, 10, 5, 10, 5, 5]
PINK = np.array([255, 200, 200])