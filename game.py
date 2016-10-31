#!/usr/bin/python3

from math import sin, cos, atan2, sqrt, pi
from random import random
import time
import copy

ENV_DECISION_TIME = 0.5 # seconds

ENV_WIDTH = 1000
ENV_HEIGHT = 1000
ENV_N_FOOD = 10
ENV_N_ANIMALS = 5

CULL_PERIOD = 10 / ENV_DECISION_TIME

ANIMAL_MOVE_DISTANCE = 5

FOOD_STRENGTH = 1

FOOD_EAT_DISTANCE = 2

class Neuron(object):
    pass

class Perceptron(Neuron):
    def __init__(self, threshold, num_inputs):
        self.w = [0 for i in range(num_inputs)] # weights

        self.threshold = threshold

    def output(self, x):
        return 1 if sum(weight * x[i] for (i, weight) in self.w) > self.threshold else 0

class Entity(object):
    def __init__(self, x, y):
        """ the position of the entity in the environment """
        self.x = x
        self.y = y

class Animal(Entity):
    """ defines an animal, which is a "species" containing a neural network """
    def __init__(self, x, y, food):
        super(Animal, self).__init__(x, y)

        """ the orientation of the animal in the environment (range: 0 to 2pi) """
        self.orientation = 0

        """ number of food eaten in this generation by tihs animal """
        self.num_food = 0

        """ inputs """
        self.smell = 0

        """ synapses """
        self.syn0 = random()

        """ outputs """
        self.out_angle = None

        self.food = food

    def breed(self):
        """ returns a new animal object (a mutated version of this one) """
        self.num_food = 0

        child = copy.deepcopy(self)

        """ TODO: randomly mutate the child here """

        return child

    def input(self):
        """
        this is run once per simulation
        this function is the entry point to the neural network belonging to this animal
        """

        """ input values """
        smell = self.get_current_smell()

        input0 = 1 if self.smell > self.smell else 0

        angle = self.syn0

        self.out_angle

        """ move in the direction of the synapse value """
        move(self.out_angle)

        """ set the strength synapse to the current smell strength """
        self.out_angle

    def get_current_smell(self):
        """ gets the current smell strength of the animal """
        smells = [food.strength / (sqrt((self.x - food.x) ** 2, (self.y - food.y) ** 2) ** 2)
                for food in self.food]

        return sum(smells)

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
        distance = ANIMAL_MOVE_DISTANCE # constant moving distance

        self.orientation += angle

        self.x += distance * cos(self.orientation)
        self.y += distance * sin(self.orientation)

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
