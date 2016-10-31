from math import sin, cos, pi
from random import random

ENV_WIDTH = 1000
ENV_HEIGHT = 1000
ENV_N_FOOD = 10

ANIMAL_MOVE_DISTANCE = 5

class Animal:
    """ defines an animal, which is a "species" of the neural network """
    def __init__(self, x, y):
        """ the position of the animal in the environment """
        self.x = x
        self.y = y

        """ the orientation of the animal in the environment (range: 0 to 2pi) """
        self.orientation = 0

    def move(self, angle):
        """ turns and moves forward by a set distance """
        distance = ANIMAL_MOVE_DISTANCE # constant moving distance

        self.x += distance * cos(angle)
        self.y += distance * sin(angle)

class Food:
    """ defines a food particle in the environment (later add taste, health etc. """
    def __init__(self, x, y):
        """ the position of the food particle in the environment """
        self.x = x
        self.y = x


class Environment:
    """ defines the environment for the simulation """
    def __init__(self):
        """ defines the 2d bounds of the environment """
        self.W = ENV_WIDTH
        self.H = ENV_HEIGHT

        """ defines the location of food particles: array of Food instances """
        self.food = []

        """ generate random food to begin with """
        self.generate_food()

    def generate_food(self):
        """ generates random food particles """
        num_food = ENV_N_FOOD

        pos = [[random() * self.W, random() * self.H] for i in range(num_food)]

        self.food += [Food(pos[i][0], pos[i][1]) for i in range(num_food)]

""" new environment """
env = Environment()

""" create a generation (generation 0) """
env.generate()
