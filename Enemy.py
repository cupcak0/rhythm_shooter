import math
import pygame as pg
import numpy as np
import random
from Functions import *
from Constant import *


class Enemy:
    def __init__(
        self, x_degrees=0, y_degrees=0, x_direction=1, y_direction=1, speed=1, health=2
    ):
        self.x_degrees = x_degrees
        self.y_degrees = y_degrees
        self.x_direction = x_direction
        self.y_direction = y_direction
        self.speed = speed
        self.health = health

    @property
    def position(self):
        x_radians = math.radians(self.x_degrees)
        y_radians = math.radians(self.y_degrees)

        p = rotate(
            FORWARD,
            math.sin(x_radians),
            math.cos(x_radians),
            math.sin(y_radians),
            math.cos(y_radians),
        )
        return p

    def move(self):
        self.x_degrees += self.x_direction * self.speed
        self.y_degrees += self.y_direction * self.speed

    def update(self):
        self.move()

    @property
    def alive(self):
        return self.health > 0

    def damage(self, amount):
        self.health -= amount


class EnemySpawner:
    @staticmethod
    def get_enemy(rand=True) -> Enemy:
        if rand:
            methods = (EnemySpawner.get_normal,)
            enemy_method = random.choice(methods)
            return enemy_method()
        else:
            return EnemySpawner.get_normal(rand=False)

    @staticmethod
    def get_normal(rand=True) -> Enemy:
        if rand:
            return Enemy(
                x_degrees=random.randint(0, 359),
                y_degrees=random.randint(-60, 60),
                x_direction=random.choice((-1, 1)) * random.random(),
                y_direction=random.choice((-1, 1)) * max(0.01, random.random()),
                speed=0.5 * random.random(),
                health=1,
            )
        else:
            return Enemy(speed=1, health=2)


class EnemySystem:
    def __init__(self, enemy_count=3):
        self.enemy_count = enemy_count
        self.enemies = []
        for i in range(self.enemy_count):
            enemy = EnemySpawner.get_enemy()
            self.enemies.append(enemy)

    def update(self):
        for id, enemy in enumerate(self.enemies):
            enemy.update()
            is_alive = enemy.alive
            if not is_alive:
                self.enemies[id] = None
                self.enemies[id] = EnemySpawner.get_enemy()

    @property
    def enemies_positions(self):
        positions = []
        for enemy in self.enemies:
            positions.append(enemy.position)
        positions = np.array(positions)
        return positions
