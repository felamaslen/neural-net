import pdb
from math import sin, cos, atan2, sqrt, pi, e
from random import random

from constants import *
from neuron import Neuron

from ann import ANN, Perceptron

class Entity(object):
    def __init__(self, x, y, W, H):
        """ the position of the entity in the environment """
        self.x = x
        self.y = y

        """ bounds of the environment """
        self.W = W
        self.H = H

class Animal(Entity):
    """ defines an animal, which is a "species" containing a neural network """
    def __init__(self, x, y, W, H, food):
        super(Animal, self).__init__(x, y, W, H)

        self.brain = ANN(THE_BRAIN, Perceptron)

        """ the orientation of the animal in the environment (range: 0 to 2pi) """
        self.orientation = 0

        """ initialise speed """
        self.speed = ANIMAL_MOVE_SPEED

        """ number of food eaten in this generation by this animal """
        self.num_food = 0

        self.food = food

        self.fullness = ANIMAL_FULLNESS

    def seed(self):
        self.brain.seed_network()

    def fire_neurons(self, input_values):
        return self.brain.run(input_values)

    def input(self):
        """ input values """
        self.fullness -= 1

        input_values = [self.get_nearest_vector()]

        """ open fire! """
        [left, turn] = self.fire_neurons(input_values)

        #go_left = left > THRESHOLD_OUTPUT and left > right
        #go_right = right > THRESHOLD_OUTPUT and right > left
        
        delta_angle = (int(left)*2-1) * ANIMAL_MOVE_ANGLE if turn else 0
        """ move in the direction of the synapse value """
        self.move(delta_angle)

        """ check if we've encountered food; if so, eat it """
        self.eat_food()

    def get_nearest_vector(self):
        """ gets the normalised vector from the animal to the nearest bit of
        food, for input to the neural network """
        if len(self.food) == 0:
            return [0]

        min_distance = -1
        min_key = -1

        for i, food in enumerate(self.food):
            distance = (self.x - food.x) ** 2 + (self.y - food.y) ** 2

            if min_distance == -1 or distance < min_distance:
                min_distance = distance

                min_key = i

        x1 = self.food[min_key].x
        y1 = self.food[min_key].y

        angle1 = atan2(y1 - self.y, x1 - self.x)

        return [angle1 - self.orientation]

    def eat_food(self):
        """ eats food if we're on top of it (defined as within a certain small distance) """
        for item in self.food:
            distance = sqrt((item.x - self.x) ** 2 + (item.y - self.y) ** 2)

            if distance < FOOD_EAT_DISTANCE:
                self.fullness += FOOD_SATIATION

                #self.fullness = min(
                #        STOMACH_SIZE, self.fullness + int(FOOD_SATIATION // self.growth)
                #    )
                self.food.remove(item)
                self.num_food += 1

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

class Food(Entity):
    """ defines a food particle in the environment (later add taste, health etc. """
    def __init__(self, x, y, W, H):
        super(Food, self).__init__(x, y, W, H)


