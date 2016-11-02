#!/usr/bin/python3
''' TODO: - Implement Continuous Time - Implement Predators - Bad food - Clean up code (imports) - Mutations based on Gaussian Distribution'''
import pdb
import sys
import select
from math import sin, cos, floor, pi
import numpy as np
from random import random, randint
import time

import tkinter

from getkey import KeyPoller

from constants import *
from learn import Entity, Animal, Food

class Environment(object):
    """ defines the environment for the simulation """
    def __init__(self):
        """ defines the 2d bounds of the environment """
        self.W = ENV_WIDTH
        self.H = ENV_HEIGHT

        self.visualise = VISUALISE

        self.generation = 0

        """ defines the location of food particles: array of Food instances """
        self.food = []

        """ defines the animals in the environment """
        self.animals = self.generate_animals()

        """ graphics window """
        self.window = tkinter.Tk()

        self.canvas = tkinter.Canvas(self.window, width = self.W, height = self.H)
        self.canvas.pack()

        """ start creating generations """
        self.generate()

        self.window.mainloop()

    def draw_display(self):
        """ displays the current environment state in the window """
        self.canvas.delete(tkinter.ALL)
        #canvas.delete(Tkinter.ALL)
        if self.visualise:
            for food in self.food:
                self.draw_food(food)

            for animal in self.animals:
                self.draw_animal(animal)

        self.draw_gui()

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

        r_head = ANIMAL_HEAD_RADIUS * animal.growth
        l_body = ANIMAL_BODY_LENGTH * animal.growth

        c_head = ANIMAL_HEAD_COLOR

        c_head = "#%02x0000" % (animal.num_food)

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

    def draw_gui(self):
        """ draws the gui """
        #w = tkinter.Label(self.canvas, text="GENERATION {} FOOD EATEN {}".format(self.generation, ENV_N_FOOD-len(self.food)), fg='white', bg='black')
        #w.place(x = 0, y = 0)
        pass

    def generate(self):
        """ start a generation """
        self.food += self.generate_food()
        while True:
            self.simulate()
            self.draw_display()

    def simulate(self):
        """ input current data to each animal """
        for thing in self.animals:
            thing.input()
            if thing.fullness == 0:
                """ kill animals which go hungry """
                self.animals.remove(thing)
                child = Animal(random() * self.W, random() * self.H, self.W, self.H, self.food)
                a1 = self.animals[randint(0,len(self.animals)-1)]
                for o in range(child.brain.layers-1):
                    for m in range(child.brain.sizes[o+1]):
                        child.brain.neurons[o][m].weights = [a1.brain.neurons[o][m].weights[i] if random()>MUTATION_RATE else random()-0.5 for i in range(len(a1.brain.neurons[o][m].weights))]
                        child.brain.neurons[o][m].bias = a1.brain.neurons[o][m].bias if random()>MUTATION_RATE else random()-0.5

                self.animals.append(child)

    def generate_food(self):
        """ generates random food particles (run once per generation) """
        num_food = ENV_N_FOOD

        pos = [(random() * self.W, random() * self.H) for i in range(num_food)]

        return [Food(x, y, self.W, self.H) for (x, y) in pos]

    def generate_animals(self):
        """ generates random animals on start (only called once) """
        num_animals = ENV_N_ANIMALS

        pos = [(random() * self.W, random() * self.H) for i in range(num_animals)]

        animallist = [Animal(x, y, self.W, self.H, self.food) for (x, y) in pos]

        for i in animallist:
            i.seed()

        return animallist

""" new environment """
env = Environment()

