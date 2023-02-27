import pygame as pg
from Camera import *
from Renderer import *
import numpy as np
from numba import njit
from Functions import *
from Constant import *
from Enemy import *


class PointSystem:
    def __init__(self, track=TRACK):
        self.points = 0
        self.shoot_count = 0
        self.track = track
        self.track_pos = 0
        self.time = 0
        self.shot = False

    def add_points(self, amount):
        self.points += amount

    def shoot(self, hit=True):
        self.shoot_count += 1
        if hit and not self.shot:
            self.add_points(self.track_points())
        self.shot = True

    def get_accuracy(self):
        if self.shoot_count == 0:
            return 1
        return self.points / self.shoot_count

    def update(self, time):
        self.time += time
        return self.track_update()

    def track_update(self):
        if self.time >= self.track[self.track_pos]:
            self.time -= self.track[self.track_pos]
            self.track_pos += 1
            if not self.shot:
                self.shoot(hit=False)
            self.shot = False
        if self.track_pos == len(self.track):
            return False
        return True

    def track_time(self):
        return self.track[self.track_pos] - self.time

    def track_points(self):
        time = self.track_time()
        if time <= 1:
            return 1
        return 0.5
