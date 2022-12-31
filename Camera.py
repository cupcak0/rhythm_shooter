import numpy as np
import pyquaternion as pq
from Functions import *


class Camera:
    def __init__(self, position=np.array([0,0,0]), fov=70, aspect=16/9, x_degrees = 0, y_degrees = 0):
        self.position = position
        self.x_degrees = x_degrees
        self.y_degrees = y_degrees
        self.fov = fov
        self.aspect = aspect

    # Поворачивает камеру на заданное количество градусов
    def rotate(self, x_degrees, y_degrees):
        self.x_degrees += x_degrees
        self.y_degrees = min(max(-90, self.y_degrees+y_degrees), 90)

    def move(self, v):
        self.position = self.position + rotate(v, self.x_degrees, self.y_degrees)