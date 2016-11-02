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
from learn import Organism

class Environment(object):
    """ defines the environment for the simulation """
    def __init__(self):
        """ defines the 2d bounds of the environment """
        self.W = ENV_WIDTH
        self.H = ENV_HEIGHT

        """ graphics window """
        self.window = tkinter.Tk()

        self.canvas = tkinter.Canvas(self.window, width = self.W, height = self.H)
        self.canvas.pack()

        """ start game loop"""
        self.generate()

        self.window.mainloop()

    def draw_display(self):
        """ displays the current environment state in the window """
        self.canvas.delete(tkinter.ALL)
        #canvas.delete(Tkinter.ALL)
        if VISUALISE:
            for organism in self.organisms:
                self.draw_organism(organism)

        self.window.update_idletasks()
        self.window.update()

    def draw_organism(self, organism):
        """ draw an organism """
        """ draw body """
        if organism.energy > INITIAL_ENERGY:
            l_body = ORGANISM_BODY_LENGTH * np.log(organism.energy - INITIAL_ENERGY + 1)
            c_body = ORGANISM_BODY_COLOR

            self.canvas.create_line(
                    organism.x, organism.y,
                    organism.x - l_body * cos(organism.orientation),
                    organism.y - l_body * sin(organism.orientation),
                    fill = c_body
                )

        """ draw head """
        r_head = ORGANISM_HEAD_SCALE * organism.size

        red = max(0, min(255, int(255 * organism.size // 10)))

        green = 255 - red

        c_head = "#%02x%02x00" % (red, green)

        self.canvas.create_oval(
                organism.x - r_head, organism.y - r_head,
                organism.x + r_head, organism.y + r_head,
                fill = c_head
            )

    def generate(self):
        """ main loop """
        self.organisms = self.generate_organisms(ENV_NUM_PLANTS)

        frame = 0
        fps_check_interval = 1000
        prev_time = time.time()

        while True:
            self.spawn_random_organisms()

            self.handle_organisms()

            self.draw_display()

            if SIMULATION_SPEED > 0:
                time.sleep(SIMULATION_SPEED)
            frame += 1

            if frame % fps_check_interval == 0:
                now = time.time()
                print("fps: {}".format(fps_check_interval // (now - prev_time)))
                prev_time = now

    def handle_organisms(self):
        """ input current data to each organism """
        for organism in self.organisms:
            organism.input()

            if organism.energy == 0:
                """ kill organisms which go hungry """
                self.organisms.remove(organism)

                """ spawn a new child from the most energetic remaining organisms """
                child = Organism(
                    random() * self.W, random() * self.H,
                    self.W, self.H,
                    self.organisms
                )

                """ inherit characteristics here """
                """ TODO: write a better cloning algorithm """
                a1 = self.organisms[randint(0,len(self.organisms)-1)]

                for o in range(child.brain.layers-1):
                    for m in range(child.brain.sizes[o+1]):
                        child.brain.neurons[o][m].weights = [
                                a1.brain.neurons[o][m].weights[i] if random() > MUTATION_RATE else random() - 0.5
                                for i in range(len(a1.brain.neurons[o][m].weights))
                            ]

                        child.brain.neurons[o][m].bias = a1.brain.neurons[o][m].bias if random()>MUTATION_RATE else random()-0.5


                self.organisms.append(child)

    def spawn_random_organisms(self):
        """ spawns new organisms (plants) at random over time """
        if random() * (ENV_NUM_PLANTS * 5 - len(self.organisms)) / ENV_NUM_PLANTS > 1 - ORGANISM_GEN_RATE:
            self.organisms.append(Organism(
                random() * self.W, random() * self.H, self.W, self.H, self.organisms
            ))

    def generate_organisms(self, number):
        """ generates random organisms initially """
        organisms = []

        for i in range(number):
            organisms.append(
                Organism(
                    random() * self.W, random() * self.H,
                    self.W, self.H,
                    organisms
                )
            )

        for organism in organisms:
            organism.seed()

        return organisms

""" new environment """
env = Environment()

