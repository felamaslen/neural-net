import pdb
from math import sin, cos, atan2, sqrt, pi, e
from random import random

from neuron import Neuron

NUM_INPUT_NEURONS = 20
NUM_OUTPUT_NEURONS = 2 # direction, speed

ANIMAL_MOVE_SPEED = 3
ANIMAL_MOVE_SPEED_MAX = 10
ANIMAL_MOVE_SPEED_MIN = 0

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
        self.num_input_neurons = NUM_INPUT_NEURONS
        self.num_output_neurons = NUM_OUTPUT_NEURONS

        """ NEURAL NETWORK: INPUT """
        """ each input neuron is dynamically weighted towards either speed or rotation """
        self.neurons_input = [
                Neuron(
                    [self.weight_seed() for j in range(self.num_output_neurons)],
                    self.neural_bias
                )
                for i in range(self.num_input_neurons)
            ]

        """ NEURAL NETWORK: OUTPUT """
        self.neurons_output = [
                Neuron([1 for i in range(self.num_input_neurons)], self.neural_bias)
                for j in range(self.num_output_neurons)
            ]

        """ number of food eaten in this generation by this animal """
        self.num_food = 0

        self.food = food

        """ inputs """
        self.smell = self.get_current_smell()

    def weight_seed(self):
        return 1 if self.is_child else random() - 0.5

    def fire_neurons(self, input_values, input_ranges, i):
        """ fire the neural network with input values """

        """ first, normalise the input values between -1 and 1 """
        input_normalised = [-1 + 2 * (value - input_ranges[k][0]) /
                (input_ranges[k][1] - input_ranges[k][0])
                for (k, value) in enumerate(input_values)]

        """ input the input values into the input neurons, get output """
        output_layer0 = [
                self.neurons_input[k].output(input_normalised)
                for k in range(self.num_input_neurons)]

        """ feed the output from the input neurons, into the output neurons """
        output = [
                self.neurons_output[k].output(output_layer0)
                for k in range(self.num_output_neurons)]

        if i == 0:
            pass#print("%0.2f -> %0.20f" % (delta, last_out_rotation))

        """ return this final output list """
        return output

    def input(self, i):
        """
        this is run once per simulation
        this function is the entry point to the neural network belonging to this animal
        """

        """ input values """
        smell = self.get_current_smell()

        """ use the difference between the smell now and the smell before,
        to determine the new angle """
        smell_delta = smell - self.smell

        input_values = [smell, smell_delta]

        """ find input ranges for normalisation """
        input_ranges = []

        """ the maximum possible smell is zero distance from all the food
        particles, all stacked on top of each other (unlikely, but possible) """
        max_smell = sum([food.strength for food in self.food])

        """ the minimum possible smell is arbitrarily far from all food particles """
        min_smell = 0

        """ range for smell """
        input_ranges.append([min_smell, max_smell])

        """ range for smell_delta (consider a jump from max to min (0) or vice versa) """
        input_ranges.append([-max_smell, max_smell])

        """ open fire! """
        out_rotation, out_speed = self.fire_neurons(input_values, input_ranges, i)

        delta_angle = 0#ANIMAL_MOVE_MAX_ANGLE * (2 * out_rotation - 1)

        self.speed += out_speed / 1000

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


