import numpy as np
import pyquaternion as pq

class Camera:
    def __init__(self, position=np.array([0,0,0]), fov=70, aspect=16/9):
        self.position = position
        self.x_degrees = 0
        self.y_degrees = 0
        self.angle = pq.Quaternion()
        self.fov = fov
        self.aspect = aspect

    # Поворачивает камеру на заданное количество градусов
    def rotate(self, x_degrees, y_degrees):
        self.x_degrees += x_degrees
        self.y_degrees += y_degrees

        angle_y = pq.Quaternion(axis=[1.0,0.0,0.0], degrees=self.y_degrees)
        angle_x = pq.Quaternion(axis=[0.0,1.0,0.0], degrees=self.x_degrees)
        
        self.angle = angle_x*angle_y