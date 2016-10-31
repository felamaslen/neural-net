#!/usr/bin/python3

from math import sin, cos, atan2, sqrt, pi, e
from random import random
import time
import copy

from learn import Entity, Animal, Food

ENV_DECISION_TIME = 0.5 # seconds

ENV_WIDTH = 1000
ENV_HEIGHT = 1000
ENV_N_FOOD = 10
ENV_N_ANIMALS = 5

CULL_PERIOD = 10 / ENV_DECISION_TIME

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
        """ start a generation """
        self.time = 0

        while self.time < CULL_PERIOD:
            self.simulate()
            self.time += ENV_DECISION_TIME
            time.sleep(ENV_DECISION_TIME)

        self.cull()
        self.generate() # new generation

    def simulate(self):
        """ input current data to each animal """
        for item in self.animals:
            item.input()

    def cull(self):
        """ remove animals that have no food """
        self.animals = [animal for animal in self.animals if animal.num_food > 0]

        for animal in self.animals:
            """ breed this animal """
            self.animals.append(animal.breed())

    def generate_food(self):
        """ generates random food particles (run once per generation) """
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
