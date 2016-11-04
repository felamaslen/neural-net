import pdb
from ann import ANN, Perceptron
from constants import *

from random import random, randint
from math import *
import numpy as np

class Organism(object):
    def __init__(self, pos):
        self.pos = pos
        self.move_to = pos
        self.speed = ORGANISM_SPEED
        self.cull = False
        self.size = ORGANISM_INITIAL_SIZE
        self.brain = ANN(ORGANISM_BRAIN, Perceptron)
        self.orientation = random()*2*pi
        self.tail_s, self.head_s = ORGANISM_TAILSIZE, ORGANISM_HEADSIZE
        self.success = 0
        self.colour = '#%02x%02x%02x' % (randint(0,255), randint(0,255), randint(0,255))

    def draw(self, canvas):
        canvas.create_line(
                self.pos[0], self.pos[1],
                self.pos[0] - self.tail_s * cos(self.orientation),
                self.pos[1] - self.tail_s * sin(self.orientation),
                fill = "black"
            )

        canvas.create_oval(
                self.pos[0] - self.head_s, self.pos[1] - self.head_s,
                self.pos[0] + self.head_s, self.pos[1] + self.head_s,
                fill = self.colour
            )

    def feed(self, food):
        self.size += food
        self.success += 1

    def update(self, inputs):
        self.size -= ORGANISM_SIZE_LOSS

        #self.size = (self.size - ORGANISM_SIZE_LOSS * self.size ** 2)

        self.size *= ORGANISM_SIZE_EFFICIENCY

        if self.size <= MINIMUM_SIZE:
            self.cull = True

        self.head_s = ORGANISM_HEADSIZE * \
                (1 + np.log(max(0, (self.size - ORGANISM_INITIAL_SIZE) / ORGANISM_INITIAL_SIZE) + 1))
        self.tail_s = ORGANISM_TAILSIZE * \
                (1 + np.log(max(0, (self.size - ORGANISM_INITIAL_SIZE) / ORGANISM_INITIAL_SIZE) + 1))

        self.speed = (self.head_s) ** 0.5 / 2;

        if not self.cull:
            [turn, direction, stop] = self.brain.run(inputs)

            delta_angle = (2 * int(direction) - 1) * ORGANISM_TURN_AMOUNT * int(turn)

            if not stop:
                self.move_to = self.move(delta_angle)

    def seed(self):
        self.brain.seed_network()

    def move(self, angle):
        """ turns and moves forward by a set distance """

        self.orientation += angle

        speed = self.speed / (1 + abs(angle))

        new_x = self.pos[0] + speed * cos(self.orientation)
        new_y = self.pos[1] + speed * sin(self.orientation)

        """ bounce off the walls """
        if new_x <= 0 or new_x >= ENV_WIDTH - 1:
            self.orientation = pi - self.orientation
            new_x = 0 if new_x <= 0 else ENV_WIDTH - 1

        if new_y <= 0 or new_y >= ENV_HEIGHT - 1:
            self.orientation *= -1
            new_y = 0 if new_y <= 0 else ENV_HEIGHT - 1

        return [new_x, new_y]
