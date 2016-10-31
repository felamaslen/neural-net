from math import sin, cos, atan2, sqrt, pi
from random import random

from neuron import Neuron

ANIMAL_MOVE_DISTANCE = 5
ANIMAL_MOVE_MAX_ANGLE = pi / 4

FOOD_STRENGTH = 1
FOOD_EAT_DISTANCE = 2

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
        self.orientation = pi / 4;

        self.neural_bias = -0.3;
        self.num_inputs = 1;

        """ create an input neuron, initialised with random weight """
        self.neuron = Neuron([random() - 0.5], self.neural_bias, self.num_inputs);

        """ number of food eaten in this generation by tihs animal """
        self.num_food = 0

        """ inputs """
        self.smell = 0

        self.food = food

    def breed(self):
        """ returns a new animal object (a mutated version of this one) """
        self.num_food = 0

        child = copy.deepcopy(self)

        child.mutate()

        return child

    def mutate(self):
        """ modify the weight of the neuron randomly """
        self.neuron.w[0] += random() * 0.1 - 0.2

    def input(self):
        """
        this is run once per simulation
        this function is the entry point to the neural network belonging to this animal
        """

        """ input values """
        smell = self.get_current_smell()

        """ use the difference between the smell now and the smell before,
        to determine the new angle """
        delta_angle = self.neuron.output([smell - self.smell])

        self.smell = smell

        """ move in the direction of the synapse value """
        self.move(delta_angle)

        """ check if we've encountered food; if so, eat it """
        self.eat_food()

    def get_current_smell(self):
        """ gets the current smell strength of the animal """
        smells = [food.strength / (sqrt((self.x - food.x) ** 2 + (self.y - food.y) ** 2) ** 2)
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

        self.x += distance * cos(self.orientation)
        self.y += distance * sin(self.orientation)

class Food(Entity):
    """ defines a food particle in the environment (later add taste, health etc. """
    def __init__(self, x, y):
        super(Food, self).__init__(x, y)

        self.strength = FOOD_STRENGTH


