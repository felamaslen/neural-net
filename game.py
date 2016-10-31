#!/usr/bin/python3

from math import sin, cos, atan2, sqrt, pi
from random import random
import time

ENV_DECISION_TIME = 0.5 # seconds

ENV_WIDTH = 1000
ENV_HEIGHT = 1000
ENV_N_FOOD = 10
ENV_N_ANIMALS = 5

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

    def simulate(self):
        """
        this is run once per simulation
        this function is the input point to the neural network belonging to this animal
        """
        pass

    def get_strongest_direction(self):
        """ returns the direction of the strongest smell """
        distance = [sqrt((self.x - food.x) ** 2, (self.y - food.y) ** 2) for food in self.food]

        angle = [atan2((food.y - self.y), (food.x - self.y)) for food in self.food]

        strongest_key = distance.index(min(distance))

        return angle[strongest_key]

    def move(self, angle):
        """ turns and moves forward by a set distance """
        distance = ANIMAL_MOVE_DISTANCE # constant moving distance

        self.x += distance * cos(angle)
        self.y += distance * sin(angle)

class Food(Entity):
    """ defines a food particle in the environment (later add taste, health etc. """
    def __init__(self, x, y):
        super(Food, self).__init__(x, y)

        self.strength = FOOD_STRENGTH

class Environment(object):
    """ defines the environment for the simulation """
    def __init__(self):
        """ defines the 2d bounds of the environment """
        self.W = ENV_WIDTH
        self.H = ENV_HEIGHT

        """ defines the location of food particles: array of Food instances """
        self.food = []

        """ defines the animals in the environment """
        self.generate_animals()

        """ generate random food to begin with """
        self.generate_food()

    def generate(self):
        self.num_simulations = 0

        while True:
            self.simulate()
            self.num_simulations += 1
            time.sleep(ENV_DECISION_TIME)

    def simulate(self):
        print("Simulation %s" % self.num_simulations)

        for item in self.animals:
            item.simulate()

    def generate_food(self):
        """ generates random food particles """
        num_food = ENV_N_FOOD

        pos = [(random() * self.W, random() * self.H) for i in range(num_food)]

        self.food += [Food(x, y) for (x, y) in pos]

    def generate_animals(self):
        """ generates random animals on start (only called once) """
        num_animals = ENV_N_ANIMALS

        pos = [(random() * self.W, random() * self.H) for i in range(num_animals)]

        self.animals = [Animal(x, y, self.food) for (x, y) in pos]

""" new environment """
env = Environment()

""" create a generation (generation 0) """
env.generate()
