from math import sin, cos, atan2, sqrt, pi
from random import random

from neuron import Neuron

ANIMAL_MOVE_DISTANCE = 5
ANIMAL_MOVE_MAX_ANGLE = pi / 4

MUTATION_RATE = 0.1
WEIGHT_SEED = 5

FOOD_STRENGTH = 1
FOOD_EAT_DISTANCE = 5

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

        """ the orientation of the animal in the environment (range: 0 to 2pi) """
        self.orientation = random() * 2 * pi

        self.neural_bias = 0
        self.num_inputs = 1

        """ create an input neuron, initialised with random weight """
        self.neuron = Neuron([WEIGHT_SEED * (random() - 0.5)], self.neural_bias, self.num_inputs)

        """ number of food eaten in this generation by tihs animal """
        self.num_food = 0

        """ inputs """
        self.smell = 0

        self.food = food

    def breed(self):
        """ returns a new animal object (a mutated version of this one) """
        self.num_food = 0

        child = Animal(self.x, self.y, self.W, self.H, self.food)
        child.orientation = self.orientation
        child.neuron.weight = self.neuron.weight

        child.mutate()

        return child

    def mutate(self):
        """ modify the weight of the neuron randomly """
        self.neuron.weight[0] += MUTATION_RATE * (random() - 0.5)

    def input(self):
        """
        this is run once per simulation
        this function is the entry point to the neural network belonging to this animal
        """

        """ input values """
        smell = self.get_current_smell()

        """ use the difference between the smell now and the smell before,
        to determine the new angle """
        smell_delta = (smell - self.smell) / smell

        neuron_output = self.neuron.output([smell_delta])

        delta_angle = ANIMAL_MOVE_MAX_ANGLE * (2 * neuron_output - 1)

        self.smell = smell

        """ move in the direction of the synapse value """
        self.move(delta_angle)

        """ check if we've encountered food; if so, eat it """
        self.eat_food()

    def get_current_smell(self):
        """ gets the current smell strength of the animal """
        smells = [food.strength / (
                    ((self.x - food.x) / self.W) ** 2 + ((self.y - food.y) / self.H) ** 2
                )
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

        self.orientation += min(ANIMAL_MOVE_MAX_ANGLE, max(-ANIMAL_MOVE_MAX_ANGLE, angle))

        new_x = self.x + distance * cos(self.orientation)
        new_y = self.y + distance * sin(self.orientation)

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


