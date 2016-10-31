#!/usr/bin/python3

from math import sin, cos
from random import random
import time

import tkinter

from learn import Entity, Animal, Food

ENV_DECISION_TIME = 0.01 # seconds

ENV_WIDTH = 1000
ENV_HEIGHT = 1000
ENV_N_FOOD = 100
ENV_N_ANIMALS = 20

CULL_PERIOD = 5 / ENV_DECISION_TIME

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

        """ defines the location of food particles: array of Food instances """
        self.food = []

        """ defines the animals in the environment """
        self.generate_animals()

        """ generate random food to begin with """
        self.generate_food()

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

        """ redraw the display, as the state changed """
        self.draw_display()

    def cull(self):
        """ remove animals that have no food """
        self.animals = [animal for animal in self.animals if animal.num_food > 0]

        num_animals = len(self.animals)
        for i in range(num_animals):
            """ breed this animal """
            self.animals.append(self.animals[i].breed())

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

