import pygame as pg
from Camera import *
from Renderer import *
import numpy as np
from numba import njit
from Functions import *
from Constant import *
from Enemy import *
from PointSystem import *


class Player:
    def __init__(
        self,
        camera=Camera(),
        enemy_system=EnemySystem(3),
        point_system=PointSystem(),
        pos=np.array([0, 0, 0]),
    ):
        self.enemy_system = enemy_system
        self.camera = camera
        self.pos = pos
        self.point_system = point_system
        self.camera.set_position(pos)

    def update(self):
        self.camera.set_position(self.pos)

    def shoot_ray(self, distance_map) -> Enemy:
        result = enemy_raymarch(
            self.pos,
            self.camera.forward_vector,
            distance_map,
            self.enemy_system.enemies,
        )
        return result

    def shoot_enemy(self, distance_map):
        enemy = self.shoot_ray(distance_map)
        if enemy is None:
            self.point_system.shoot(False)
            return
        enemy.damage(1)
        self.point_system.shoot()
