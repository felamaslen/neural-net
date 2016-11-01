#!/usr/bin/python3

import sys
from math import sin, cos, floor
from random import random
import time

import tkinter

from learn import Entity, Animal, Food

SIMULATION_SPEED = 0.01 # seconds
CULL_PERIOD = 2 / SIMULATION_SPEED

ENV_WIDTH = 500
ENV_HEIGHT = 500
ENV_N_FOOD = 50
ENV_N_ANIMALS = 20

MUTATION_RATE = 0.1

FOOD_RADIUS = 3
FOOD_COLOR = "yellow"

ANIMAL_HEAD_RADIUS  = 5
ANIMAL_HEAD_COLOR   = "red"
ANIMAL_BODY_LENGTH  = 15
ANIMAL_BODY_COLOR   = "black"

class Environment(object):
    """ defines the environment for the simulation """
    def __init__(self):
        """ defines the 2d bounds of the environment """
        self.W = ENV_WIDTH
        self.H = ENV_HEIGHT

        self.generation = 0

        """ defines the location of food particles: array of Food instances """
        self.food = []

        """ defines the animals in the environment """
        self.generate_animals()

        """ graphics window """
        self.window = tkinter.Tk()

        self.canvas = tkinter.Canvas(self.window, width = self.W, height = self.H)
        self.canvas.pack()

        """ start creating generations """
        self.generate()

        self.window.mainloop()

    def draw_display(self):
        """ displays the current environment state in the window """
        self.canvas.delete("all")

        for food in self.food:
            self.draw_food(food)

        for animal in self.animals:
            self.draw_animal(animal)

        self.window.update_idletasks()
        self.window.update()

    def draw_food(self, food):
        """ draw a piece of food """
        radius = FOOD_RADIUS
        color = FOOD_COLOR

        self.canvas.create_oval(
                food.x - radius, food.y - radius,
                food.x + radius, food.y + radius,
                fill = color)

    def draw_animal(self, animal):
        """ draw an animal """
        r_head = ANIMAL_HEAD_RADIUS
        l_body = ANIMAL_BODY_LENGTH

        c_head = ANIMAL_HEAD_COLOR
        c_body = ANIMAL_BODY_COLOR

        """ draw body """
        self.canvas.create_line(
                animal.x, animal.y,
                animal.x - l_body * cos(animal.orientation), animal.y - l_body * sin(animal.orientation),
                fill = c_body)

        """ draw head """
        self.canvas.create_oval(
                animal.x - r_head, animal.y - r_head,
                animal.x + r_head, animal.y + r_head,
                fill = c_head)

    def generate(self):
        """ start a generation """
        self.time = 0

        print("Generation %d" % self.generation)
        self.generation += 1

        """ generate random food """
        del self.food[:]
        self.generate_food()

        i = 0
        while i < CULL_PERIOD:
            self.simulate()
            i += 1
            time.sleep(SIMULATION_SPEED)

        self.cull()

        if len(self.animals) == 0:
            print("You went extinct! :(")
            sys.exit()

        self.generate() # new generation

    def simulate(self):
        """ input current data to each animal """
        i = 0
        for item in self.animals:
            item.input(i)
            i = 1

        """ redraw the display, as the state changed """
        self.draw_display()

    def cull(self):
        """ kill the worst third of the animals """
        self.animals.sort(key = lambda x: x.num_food)

        del self.animals[:floor(len(self.animals) / 3)]

        self.breed()

    def breed(self):
        """ combine the remaining animals in pairs """
        num_animals = len(self.animals)
        i = 0
        for animal in self.animals:
            if i > num_animals - 2:
                break

            if i % 2 == 0:
                a1 = self.animals[i]
                a2 = self.animals[i + 1]

                child = Animal(0.5 * (a1.x + a2.x), 0.5 * (a1.y + a2.y), self.W, self.H, self.food, True)

                """ combine and mutate children """
                child.neuron_out_rotation.apply_weight([MUTATION_RATE * (random() - 0.5) + 0.5 * (
                    a1.neuron_out_rotation.weight[i] + a2.neuron_out_rotation.weight[i]
                ) for i in range(child.num_middle_neurons)])

                child.neuron_out_speed.apply_weight([MUTATION_RATE * (random() - 0.5) + 0.5 * (
                    a1.neuron_out_speed.weight[i] + a2.neuron_out_speed.weight[i]
                ) for i in range(child.num_middle_neurons)])

                self.animals.append(child)
            i += 1

    def generate_food(self):
        """ generates random food particles (run once per generation) """

        num_food = ENV_N_FOOD

        pos = [(random() * self.W, random() * self.H) for i in range(num_food)]

        self.food += [Food(x, y, self.W, self.H) for (x, y) in pos]

    def generate_animals(self):
        """ generates random animals on start (only called once) """
        num_animals = ENV_N_ANIMALS

        pos = [(random() * self.W, random() * self.H) for i in range(num_animals)]

        self.animals = [Animal(x, y, self.W, self.H, self.food) for (x, y) in pos]

""" new environment """
env = Environment()

