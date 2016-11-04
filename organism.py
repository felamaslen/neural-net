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
        self.tail_s, self.leg_s, self.head_s = ORGANISM_TAILSIZE, ORGANISM_LEGSIZE, ORGANISM_HEADSIZE
        self.success = 0
        self.colour = '#%02x%02x%02x' % (randint(0,255), randint(0,255), randint(0,255))

        self.leg_crawl = [0] * 6

    def coord_transform(self, objects):
        """ transforms coords by current orientation """
        cosT = cos(self.orientation - pi / 2)
        sinT = sin(self.orientation - pi / 2)

        return [
            [
                [
                    self.pos[0] + cosT * x - sinT * y,
                    self.pos[1] + sinT * x + cosT * y
                ]
                for (x, y) in group
            ]
            for group in objects
        ]

    def get_legs(self):
        """ gets array of coordinates to draw legs """

        leg_pos = [
            self.tail_s * 0.1,
            self.tail_s * 0.3,
            self.tail_s * 0.5
        ]

        legs = [
                [
                    [0, -self.tail_s + leg_pos[j]],
                    [self.leg_s / LEG_JOINT, -self.tail_s + leg_pos[j]]
                ] +
                [
                    [self.leg_s / LEG_JOINT, -self.tail_s + leg_pos[j]],
                    [self.leg_s, -self.tail_s + leg_pos[j] - \
                            self.leg_crawl[j * 2] * self.leg_s * CRAWL_RATIO]
                ] +
                [
                    [0, -self.tail_s + leg_pos[j]],
                    [-self.leg_s / LEG_JOINT, -self.tail_s + leg_pos[j]]
                ] +
                [
                    [-self.leg_s / LEG_JOINT, -self.tail_s + leg_pos[j]],
                    [-self.leg_s, -self.tail_s + leg_pos[j] - \
                            self.leg_crawl[j * 2 + 1] * self.leg_s * CRAWL_RATIO]
                ]
                for j in range(3)
            ]

        coords = legs

        """ transform the coordinates """
        return self.coord_transform(coords)

    def draw(self, canvas):
        """ draw body """
        canvas.create_line(
                self.pos[0], self.pos[1],
                self.pos[0] - self.tail_s * cos(self.orientation),
                self.pos[1] - self.tail_s * sin(self.orientation),
                fill = "black"
            )

        """ draw legs """
        legs = self.get_legs()

        for leg in legs:
            for i in range(len(leg) // 2):
                canvas.create_line(leg[2*i][0], leg[2*i][1], leg[2*i+1][0], leg[2*i+1][1], fill = "black")

        """ draw head """
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

        size_scale = 1 + np.log(max(0, (self.size - ORGANISM_INITIAL_SIZE) / \
                ORGANISM_INITIAL_SIZE) + 1)

        self.head_s = ORGANISM_HEADSIZE * size_scale
        self.tail_s = ORGANISM_TAILSIZE * size_scale
        self.leg_s  = ORGANISM_LEGSIZE  * size_scale

        if not self.cull:
            [l1, l2, l3, r1, r2, r3] = self.brain.run(inputs)

            left = [l1, l2, l3]
            left.sort()

            right = [r1, r2, r3]
            right.sort()

            for j in range(3):
                self.leg_crawl[4-2*j] = left[j]
                self.leg_crawl[5-2*j] = right[j]

            self.speed = sum(self.leg_crawl) * self.leg_s ** 0.5 * CRAWL_SPEED

            turn_left = self.leg_crawl[0] + self.leg_crawl[1] + self.leg_crawl[2]
            turn_right = self.leg_crawl[3] + self.leg_crawl[4] + self.leg_crawl[5]

            turn = turn_right - turn_left

            delta_angle = turn * ORGANISM_TURN_AMOUNT

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
