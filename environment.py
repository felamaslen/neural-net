import tkinter

from constants import *
from organism import Organism
from random import random, randint
from math import *
import numpy as np
from time import sleep

class Environment(object):
    def __init__(self):
        """Set environment's dimensions"""
        self.dims = [ENV_WIDTH, ENV_HEIGHT]

        """Set up window"""
        self.setup_screen()

        """Start simulation"""
        self.run_loop()

    def setup_screen(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width = self.dims[0], height = self.dims[1])
        self.canvas.pack()

    def run_loop(self):
        self.organisms = []
        self.framecounter = 0

        while True:
            self.handle_organisms()

            self.draw()

            if not self.framecounter % 25:# and len(self.organisms) < ENV_MAX_ORGANISMS:   #spawn a new organism every 100 frames
                self.spawn_organism()
            self.framecounter += 1
            if SLOW_DOWN: sleep(SLOW_DOWN)

    def spawn_organism(self):
        if len(self.organisms) <= 5:    #ramdom organism if we dont yet have 5 organisms in the system
            self.organisms += [Organism([random()*self.dims[0], random()*self.dims[1]])]
            self.organisms[-1].seed()      #completely random organism if no organisms alive
        else:
            self.organisms.sort(key=lambda x: x.success) #choose random organism in the top 5 based on lifetime food eaten
            parent = self.organisms[randint(len(self.organisms)-2, len(self.organisms)-1)]

            child = Organism([random()*self.dims[0], random()*self.dims[1]])

            for o in range(child.brain.layers-1):
                for m in range(child.brain.sizes[o+1]):
                    child.brain.neurons[o][m].weights = [
                            parent.brain.neurons[o][m].weights[i] if random() > MUTATION_RATE else random() - 0.5
                            for i in range(len(parent.brain.neurons[o][m].weights))
                        ]
            child.brain.neurons[o][m].bias = parent.brain.neurons[o][m].bias if random()>MUTATION_RATE else random()-0.5

            self.organisms += [child]

    def eat(self, organism):
        organism.feed(100)

    def eaten(self, organism):
        organism.cull = True

    def handle_organisms(self):
        for organism in self.organisms:

            """ eat other organisms """
            input_food = self.get_closest(organism, lambda x: x.size < organism.size, self.eat)

            """ get eaten by other organisms """
            input_enemy = self.get_closest(organism, lambda x: x.size > organism.size, self.eaten)

            organism.update(input_enemy + input_food)

        self.cull()

    def get_closest(self, organism, criteria, run):
        temp = list(filter(criteria, self.organisms))

        min_distance = -1
        min_index = -1

        for index, candidate in enumerate(temp):
            dist = (candidate.pos[0]-organism.pos[0])**2+(candidate.pos[1]-organism.pos[1])**2
            if min_distance == -1 or dist < min_distance:
                min_distance = dist
                min_index = index

        if min_index != -1:
            angle = (atan2(
                temp[min_index].pos[0] - organism.pos[0],
                temp[min_index].pos[1] - organism.pos[1]) - organism.orientation) % (2 * pi)

            if min_distance < EAT_DISTANCE_SQ:
                run(organism)

            return [min_distance / ENV_MAX_DISTANCE_SQ, angle]

        return [ENV_MAX_DISTANCE_SQ, 0]

    def cull(self):
        for organism in self.organisms:
            if organism.cull:
                self.organisms.remove(organism)
            else:
                organism.pos[0], organism.pos[1] = organism.move_to[0], organism.move_to[1]


    def draw(self):
        self.canvas.delete(tkinter.ALL)

        if VISUALISE:
            for organism in self.organisms:
                organism.draw(self.canvas)

        self.window.update_idletasks()
        self.window.update()
