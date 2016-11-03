from ann import ANN, Perceptron
from constants import *

from random import random
from math import *


class Organism(object):
    def __init__(self, pos, envdims):
        self.pos = pos
        self.envdims = envdims
        self.cull = False
        self.size = 5
        self.brain = ANN(ORGANISM_BRAIN, Perceptron)
        self.orientation = random()*2*pi

    def draw(self, canvas):
        canvas.create_line(
                self.pos[0], self.pos[1],
                self.pos[0] - ORGANISM_TAILSIZE * cos(self.orientation),
                self.pos[1] - ORGANISM_TAILSIZE * sin(self.orientation),
                fill = "black"
            )

        canvas.create_oval(
                self.pos[0] - ORGANISM_HEADSIZE, self.pos[1] - ORGANISM_HEADSIZE,
                self.pos[0] + ORGANISM_HEADSIZE, self.pos[1] + ORGANISM_HEADSIZE,
                fill = "red"
            )

    def feed(self, food):
        self.size += food

    def update(self, inputs):
        self.size += PHOTOSYNTHESIS_RATE
        self.size *= ORGANISM_SIZE_LOSS

        if self.size == 0:
            self.cull = True

        [turn, direction] = self.brain.run(inputs)

        delta_angle = turn*(2*direction - 1)*ORGANISM_TURN_AMOUNT

        self.move(delta_angle)

    def seed(self):
        self.brain.seed_network()

    def move(self, angle):
        """ turns and moves forward by a set distance """
        self.orientation += angle

        new_x = max(min(self.pos[0] + ORGANISM_SPEED * cos(self.orientation), ENV_WIDTH), 0)
        new_y = max(min(self.pos[1] + ORGANISM_SPEED * sin(self.orientation), ENV_HEIGHT), 0)

        self.pos[0] = new_x
        self.pos[1] = new_y
