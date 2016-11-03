import pdb
from math import sin, cos, atan2, sqrt, pi, e
import numpy as np
from random import random

from constants import *
from neuron import Neuron

from ann import ANN, Perceptron

class Organism(object):
    """ defines an organism, which is a "species" containing a neural network """

    """ it starts out as a "plant", growing constantly wrt time, then once it reaches
    a certain size, it may start to move and eat other organisms """
    def __init__(self, x, y, W, H, others):
        """ the position of the entity in the environment """
        self.x = x
        self.y = y

        """ bounds of the environment """
        self.W = W
        self.H = H

        self.brain = ANN(THE_BRAIN, Perceptron)

        """ the orientation of the organism in the environment (range: 0 to 2pi) """
        self.orientation = 0

        """ other oganisms in the environment """
        self.others = others

        """ intialise with the size and characteristics of a plant """

        """ initialise speed (0 for plants) """
        self.speed = 0

        self.hunger = INITIAL_HUNGER

        self.size   = SIZE_PLANT

        self.num_eaten = 0

    def seed(self):
        self.brain.seed_network()

    def fire_neurons(self, input_values):
        return self.brain.run(input_values)

    def input(self):
        """ grow the oganism """
        self.size = (self.size + GROWTH_RATE) * GROWTH_EFFICIENCY

        self.hunger += 0.1

        """ set the speed according to the size """
        self.speed = 0 if self.size <= SIZE_PLANT else self.size / 4

        """ input values """

        """ get input vector for the brain """
        input_values = self.get_input_vector()

        """ open fire! """
        [direction, turn] = self.fire_neurons(input_values)

        """ move in the direction of the synapse value """
        delta_angle = (2 * int(direction) - 1) * ORGANISM_MOVE_ANGLE if turn else 0

        self.move(delta_angle)

        """ check if we've encountered food; if so, eat it """
        self.eat_others()

    def get_closest(self, others):
        """ returns the angle to the closest organism in others """
        angle = 0

        if len(others) > 0:
            min_distance = -1
            min_key = -1

            for (i, other) in enumerate(others):
                if not other is self:
                    distance = (self.x - other.x) ** 2 + (self.y - other.y) ** 2

                    if min_distance == -1 or distance < min_distance:
                        min_distance = distance
                        min_key = i

            x1 = others[min_key].x
            y1 = others[min_key].y

            angle = atan2(y1 - self.y, x1 - self.x)

        return angle - self.orientation

    def get_input_vector(self):
        """ gets all the inputs for the brain, based on current parameters """

        """ get the closest source of food """
        """ others are food if they can fit in our stomach """
        closest_food = self.get_closest(list(filter(
                lambda other: other.size < self.size * STOMACH_SIZE, self.others
            )))

        """ get the closest enemy """
        """ others are enemies if we can fit in their stomach """
        closest_enemy = self.get_closest(list(filter(
                lambda other: other.size * STOMACH_SIZE >= self.size, self.others
            )))

        return [closest_food, closest_enemy]

    def eat_others(self):
        """ checks if any other organisms can be eaten by this one """
        stomach_remaining = STOMACH_SIZE * self.size

        for other in self.others:
            if other.size < stomach_remaining and (
                (other.x - self.x) ** 2 + (other.y - self.y) ** 2 <
                (self.size / 2) ** 2
            ):
                """ this organism fits in our stomach and is close enough to be
                eaten, so we eat it. """

                """ put it in our stomach """
                stomach_remaining -= other.size

                self.hunger = max(0, self.hunger - other.size)

                """ digest it """
                self.size += DIGESTION_EFFICIENCY / other.size

                """ remove the eaten item from the others array """
                self.others.remove(other)

    def move(self, angle):
        """ turns and moves forward by a set distance """
        self.orientation += angle

        new_x = self.x + self.speed * cos(self.orientation)
        new_y = self.y + self.speed * sin(self.orientation)

        """ bounce off the walls """
        if new_x <= 0 or new_x >= self.W - 1:
            self.orientation = pi - self.orientation
            new_x = 0 if new_x <= 0 else self.W - 1

        if new_y <= 0 or new_y >= self.H - 1:
            self.orientation *= -1
            new_y = 0 if new_y <= 0 else self.H - 1

        self.x = new_x
        self.y = new_y


