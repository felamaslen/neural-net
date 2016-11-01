import pdb
from math import sin, cos, atan2, sqrt, pi, e
from random import random

from neuron import Neuron

NUM_MIDDLE_NEURONS = 20

ANIMAL_MOVE_SPEED = 5
ANIMAL_MOVE_MAX_ANGLE = pi / 4

NUM_CHILDREN = 1

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
    def __init__(self, x, y, W, H, food, child = False):
        super(Animal, self).__init__(x, y, W, H)

        self.is_child = child

        """ the orientation of the animal in the environment (range: 0 to 2pi) """
        self.orientation = random() * 2 * pi

        """ initialise speed with a randomised value """
        self.speed = ANIMAL_MOVE_SPEED * 0.5 * (1 + random())

        self.neural_bias = 0

        """ NEURAL NETWORK STRUCTURE DEFINITION """
        self.num_middle_neurons = NUM_MIDDLE_NEURONS

        """ NEURAL NETWORK: INPUT """
        """ create an input neuron, initialised with random weight """
        self.neuron_input = Neuron([1], self.neural_bias)

        """ NEURAL NETWORK: HIDDEN LAYER """
        seed_rotation = 0 if self.is_child else random()
        seed_speed = 0 if self.is_child else random()

        self.neuron_rotation    = Neuron([1], self.neural_bias) # rotation
        self.neuron_speed       = Neuron([1], self.neural_bias) # speed

        """ middle neurons handle input from both rotation and speed neurons """
        """ each middle neuron is weighted staticly towards either speed or rotation """
        self.neurons_middle = [
                Neuron([
                    1 - i / (self.num_middle_neurons - 1),
                    i / (self.num_middle_neurons - 1)
                ], self.neural_bias)
                for i in range(self.num_middle_neurons)
            ]

        """ NEURAL NETWORK: OUTPUT """
        weights_rotation = []
        for i in range(self.num_middle_neurons):
            weights_rotation.append(self.weight_seed())

        self.neuron_out_rotation = Neuron(weights_rotation, self.neural_bias)

        weights_speed = []
        for i in range(self.num_middle_neurons):
            weights_speed.append(self.weight_seed())

        self.neuron_out_speed = Neuron(weights_speed, self.neural_bias)

        """ number of food eaten in this generation by this animal """
        self.num_food = 0

        self.food = food

        """ inputs """
        self.smell = self.get_current_smell()

    def weight_seed(self):
        return 1 if self.is_child else random() - 0.5

    def fire_neurons(self, delta, i):
        """ inputs delta into the neural network, gets output """

        """
        delta is the actual smell difference;
        it must be normalised between -1 and 1

        the maximum theoretical "jump" is from right next to all the food particles
        (if they are on top of each other) to a point arbitrarily far from all the
        food particles (or vice versa)
        """
        max_delta = sum([food.strength for food in self.food])
        min_delta = 0#-max_delta

        delta_norm = -1 + 2 * (delta - min_delta) / (max_delta - min_delta)

        first_input = self.neuron_input.output([delta_norm])

        first_out_rotation  = self.neuron_rotation.output([first_input])
        first_out_speed     = self.neuron_speed.output([first_input])

        mid_out = [self.neurons_middle[i].output([first_out_rotation, first_out_speed])
                for i in range(self.num_middle_neurons)]

        last_out_rotation   = self.neuron_out_rotation.output(mid_out)
        last_out_speed      = self.neuron_out_speed.output(mid_out)

        if i == 0:
            print("%0.2f -> %0.20f" % (delta, last_out_rotation))

        return last_out_rotation, last_out_speed

    def input(self, i):
        """
        this is run once per simulation
        this function is the entry point to the neural network belonging to this animal
        """

        """ input values """
        smell = self.get_current_smell()

        """ use the difference between the smell now and the smell before,
        to determine the new angle """
        smell_delta = smell# - self.smell

        """ open fire! """
        neuron_out_rotation, neuron_out_speed = self.fire_neurons(smell_delta, i)

        delta_angle = ANIMAL_MOVE_MAX_ANGLE * (2 * neuron_out_rotation - 1)

        self.speed += neuron_out_speed / 1000

        self.smell = smell

        """ move in the direction of the synapse value """
        self.move(delta_angle)

        """ check if we've encountered food; if so, eat it """
        self.eat_food()

    def get_current_smell(self):
        """ gets the current smell strength of the animal """
        smells = [food.strength * pow(
                e, -(((self.x - food.x) / self.W) ** 2 + ((self.y - food.y) / self.H) ** 2)
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


