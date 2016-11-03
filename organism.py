import pdb
from ann import ANN, Perceptron
from constants import *

from random import random
from math import *
import numpy as np

class Organism(object):
    def __init__(self, pos):
        self.pos = pos
        self.move_to = pos
        self.cull = False
        self.size = ORGANISM_INITIAL_SIZE
        self.brain = ANN(ORGANISM_BRAIN, Perceptron)
        self.orientation = random()*2*pi
        self.tail_s, self.head_s = ORGANISM_TAILSIZE, ORGANISM_HEADSIZE
        self.success = 0

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
                fill = "red"
            )

    def feed(self, food):
        self.size += food
        self.success += 1

    def update(self, inputs):
        #self.size += PHOTOSYNTHESIS_RATE
        self.size -= ORGANISM_SIZE_LOSS                     #simple linear size loss

        self.size *= ORGANISM_SIZE_EFFICIENCY

        if self.size <= 0:
            self.cull = True

        self.head_s = ORGANISM_HEADSIZE * \
                (1 + np.log(max(-0.5, (self.size - ORGANISM_INITIAL_SIZE) / ORGANISM_INITIAL_SIZE) + 1))
        self.tail_s = ORGANISM_TAILSIZE * \
                (1 + np.log(max(-0.5, (self.size - ORGANISM_INITIAL_SIZE) / ORGANISM_INITIAL_SIZE) + 1))

        if not self.cull:
            normalised = self.normalise(inputs)

            #print(inputs)

            [turn, direction] = self.brain.run(inputs[3:])

            delta_angle = (2*int(direction) - 1)*ORGANISM_TURN_AMOUNT if turn else 0

            self.move_to = self.move(delta_angle)

    def normalise(self, inputs):
        return [
          inputs[0] / (ENV_WIDTH ** 2 + ENV_HEIGHT ** 2),
          inputs[1] % (2 * pi) / (2 * pi),

          inputs[2] / (ENV_WIDTH ** 2 + ENV_HEIGHT ** 2),
          inputs[3] % (2 * pi) / (2 * pi)
        ]

    def seed(self):
        self.brain.seed_network()

    def move(self, angle):
        """ turns and moves forward by a set distance """
        self.orientation += angle
        new_x = self.pos[0] + ORGANISM_SPEED * cos(self.orientation)
        new_y = self.pos[1] + ORGANISM_SPEED * sin(self.orientation)

        """ bounce off the walls """
        if new_x <= 0 or new_x >= ENV_WIDTH - 1:
            self.orientation = pi - self.orientation
            new_x = 0 if new_x <= 0 else ENV_WIDTH - 1

        if new_y <= 0 or new_y >= ENV_HEIGHT - 1:
            self.orientation *= -1
            new_y = 0 if new_y <= 0 else ENV_HEIGHT - 1

        return [new_x, new_y]
