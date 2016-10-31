from math import sin, cos, pi
from random import random

ENV_WIDTH = 1000
ENV_HEIGHT = 1000
ENV_N_FOOD = 10

ANIMAL_MOVE_DISTANCE = 5

FOOD_STRENGTH = 1

class Entity(object):
    def __init__(self, x, y):
        """ the position of the entity in the environment """
        self.x = x
        self.y = y

class Animal(Entity):
    """ defines an animal, which is a "species" of the neural network """
    def __init__(self, x, y, food):
        super(Animal, self).__init__(x, y)

        """ the orientation of the animal in the environment (range: 0 to 2pi) """
        self.orientation = 0

        """ this is where the magic happens """
        self.neurons = []

        self.food = food

    def get_strongest_direction(self):
        """ returns the direction of the strongest smell """
        relative_pos_strength = [
            (
                sqrt(pow(self.x - food.x, 2) + pow(self.y - food.y, 2)),
                atan((food.y - self.y) / (food.x - self.y))
            )
            for food in self.food
        ]

        smell = [1 / (pow(distance + 1, 2)) for (distance, angle) in relative_pos]

        food_key = smell.index(max(smell))

        return relative_pos_strength[food_key][1]

    def move(self, angle):
        """ turns and moves forward by a set distance """
        distance = ANIMAL_MOVE_DISTANCE # constant moving distance

        self.x += distance * cos(angle)
        self.y += distance * sin(angle)

class Food(Entity):
    """ defines a food particle in the environment (later add taste, health etc. """
    def __init__(self, x, y):
        super(Animal, self).__init__(x, y)

        self.strength = FOOD_STRENGTH

class Environment(object):
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

        pos = [(random() * self.W, random() * self.H) for i in range(num_food)]

        self.food = [Food(x, y) for (x, y) in pos]

""" new environment """
env = Environment()

""" create a generation (generation 0) """
env.generate()
