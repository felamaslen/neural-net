import pdb
from math import sin, cos, atan2, sqrt, pi, e
from random import random

from constants import *
from neuron import Neuron

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
    def __init__(self, x, y, W, H, food, child = False):
        super(Animal, self).__init__(x, y, W, H)

        self.is_child = child

        """ the orientation of the animal in the environment (range: 0 to 2pi) """
        self.orientation = 0

        """ initialise speed with a randomised value """
        self.speed = ANIMAL_MOVE_SPEED

        self.neural_bias = 0

        """ NEURAL NETWORK STRUCTURE DEFINITION """
        self.num_hidden_neurons = NUM_HIDDEN_NEURONS

        """ hidden layer """
        self.neurons_hidden = [
                Neuron(
                    [self.seed() for j in range(NUM_INPUTS)],
                    self.seed()
                )
                for i in range(self.num_hidden_neurons)
            ]

        """ output layer """
        self.neurons_output = [
                Neuron(
                    [self.seed() for j in range(self.num_hidden_neurons)],
                    self.seed()
                )
                for i in range(NUM_OUTPUTS)
            ]

        """ number of food eaten in this generation by this animal """
        self.num_food = 0

        self.food = food

    def seed(self):
        return 1 if self.is_child else random() - 0.5

    def fire_neurons(self, input_values):
        """ fire the neural network with input values """

        """ input the values to the hidden layer, get their outputs """
        hidden_out = [
                self.neurons_hidden[k].output(input_values)
                for k in range(NUM_HIDDEN_NEURONS)
            ]

        """ input those outputs to the output neurons """
        out = [
                self.neurons_output[k].output(hidden_out)
                for k in range(NUM_OUTPUTS)
            ]

        """ return this final output list """
        return out

    def input(self):
        """
        this is run once per simulation
        this function is the entry point to the neural network belonging to this animal
        """

        """ input values """
        input_values = self.get_nearest_vector()

        """ open fire! """
        left, right = self.fire_neurons(input_values)

        go_left = left > THRESHOLD_OUTPUT and left > right
        go_right = right > THRESHOLD_OUTPUT and right > left

        delta_angle = 0

        if left > THRESHOLD_OUTPUT:
            delta_angle = ANIMAL_MOVE_ANGLE

        if right > THRESHOLD_OUTPUT:
            if right > left:
                delta_angle *= -1
            else:
                delta_angle = -ANIMAL_MOVE_ANGLE

        """ move in the direction of the synapse value """
        self.move(delta_angle)

        """ check if we've encountered food; if so, eat it """
        self.eat_food()

    def get_nearest_vector(self):
        """ gets the normalised vector from the animal to the nearest bit of
        food, for input to the neural network """
        if len(self.food) == 0:
            return [1, 0]

        min_distance = -1
        min_key = -1

        for (i, food) in enumerate(self.food):
            distance = (self.x - food.x) ** 2 + (self.y - food.y) ** 2

            if min_distance == -1 or distance < min_distance:
                min_distance = distance

                min_key = i

        x1 = self.food[min_key].x
        y1 = self.food[min_key].y

        angle1 = atan2(y1 - self.y, x1 - self.x)

        return angle1 - self.orientation

    def eat_food(self):
        """ eats food if we're on top of it (defined as within a certain small distance) """
        for item in self.food:
            distance = sqrt((item.x - self.x) ** 2 + (item.y - self.y) ** 2)

            eaten = distance < FOOD_EAT_DISTANCE

            if eaten:
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

        self.strength = FOOD_STRENGTH


