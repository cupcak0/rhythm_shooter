import numpy as np
from Functions import *
from Constant import *


class Camera:
    def __init__(self, fov=70, aspect=16 / 9, x_degrees=0, y_degrees=0):
        self.x_const = -fov * aspect / 2
        self.y_const = -fov / 2
        self.x_degrees = x_degrees + self.x_const
        self.y_degrees = y_degrees + self.y_const
        self.fov = fov
        self.aspect = aspect

    # Поворачивает камеру на заданное количество градусов
    def rotate(self, x_degrees, y_degrees):
        self.x_degrees += x_degrees
        self.y_degrees = min(
            max(-70 + self.y_const, self.y_degrees + y_degrees), 70 + self.y_const
        )

    def set_position(self, position):
        self.position = position

    @property
    def forward_vector(self):
        return self.vector_rotate(FORWARD)

    @property
    def right_vector(self):
        return self.vector_rotate(RIGHT)

    @property
    def up_vector(self):
        return self.vector_rotate(UP)

    def vector_rotate(self, v):
        sin_x, cos_x = math.sin(math.radians(self.x_degrees - self.x_const)), math.cos(
            math.radians(self.x_degrees - self.x_const)
        )
        sin_y, cos_y = math.sin(math.radians(self.y_degrees - self.y_const)), math.cos(
            math.radians(self.y_degrees - self.y_const)
        )
        return rotate(v, sin_x, cos_x, sin_y, cos_y)
    
    def mvector_rotate(self, v):
        sin_x, cos_x = math.sin(math.radians(- self.x_degrees + self.x_const)), math.cos(
            math.radians(- self.x_degrees + self.x_const)
        )
        sin_y, cos_y = math.sin(math.radians(- self.y_degrees + self.y_const)), math.cos(
            math.radians(- self.y_degrees + self.y_const)
        )
        return rotate(v, sin_x, cos_x, sin_y, cos_y)
