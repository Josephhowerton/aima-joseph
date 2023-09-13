from agents import *
from things.thing import *
from environments.environment import Direction
from time import sleep


class VacuumActions:
    CLEAN_DIRT = 1
    TURN_RIGHT = 2
    TURN_LEFT = 3
    REST = 4


class Vacuum(Agent):
    def __init__(self, program):
        super().__init__(program=program)
        self.location = [0, 0]
        self.direction = Direction.R

    def clean_dirt(self, thing):
        return isinstance(thing, Dirt)

    def turn(self, d):
        self.direction = self.direction + d

    def rest(self, delay=3):
        sleep(delay)
