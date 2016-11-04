import tkinter

from constants import *
from organism import Organism
from random import random, randint
from math import *
import numpy as np
from time import sleep

LINES_DEBUG = []

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

            if not self.framecounter % SPAWN_FREQUENCY and len(self.organisms) < ENV_MAX_ORGANISMS:   #spawn a new organism every 100 frames
                self.spawn_organism()
            self.framecounter += 1
            if SLOW_DOWN: sleep(SLOW_DOWN)

    def spawn_organism(self):
        if len(self.organisms) <= 5:    #ramdom organism if we dont yet have 5 organisms in the system
            self.organisms += [Organism([random()*self.dims[0], random()*self.dims[1]])]
            self.organisms[-1].seed()      #completely random organism if no organisms alive
        else:
            self.organisms.sort(key=lambda x: x.size) #choose random organism in the top 5 based on lifetime food eaten
            parent = self.organisms[randint(len(self.organisms)-5, len(self.organisms)-1)]

            child = Organism([random()*self.dims[0], random()*self.dims[1]])

            for o in range(child.brain.layers-1):
                for m in range(child.brain.sizes[o+1]):
                    child.brain.neurons[o][m].weights = [
                            parent.brain.neurons[o][m].weights[i] \
                                    if random() > MUTATION_RATE else random() - 0.5
                            for i in range(len(parent.brain.neurons[o][m].weights))
                        ]
            child.brain.neurons[o][m].bias = parent.brain.neurons[o][m].bias \
                    if random() > MUTATION_RATE else random()-0.5

            self.organisms += [child]

    def eat(self, this, that):
        this.feed(FEED_AMOUNT)
        that.cull = True

    def eaten(self, this, that):
        pass

    def handle_organisms(self):
        del LINES_DEBUG[:]
        for organism in self.organisms:
            """ eat other organisms """
            input_food = self.get_closest(organism, lambda x: x.size < organism.size, self.eat)

            """ get eaten by other organisms """
            input_enemy = self.get_closest(organism, lambda x: x.size > organism.size, self.eaten)

            LINES_DEBUG.append([
                [
                    organism.pos[0], organism.pos[1],
                    organism.pos[0] + input_food[2] ** 0.5 * cos(input_food[3]),
                    organism.pos[1] + input_food[2] ** 0.5 * sin(input_food[3])
                ],
                [
                    organism.pos[0], organism.pos[1],
                    organism.pos[0] + input_enemy[2] ** 0.5 * cos(input_enemy[3]),
                    organism.pos[1] + input_enemy[2] ** 0.5 * sin(input_enemy[3])
                ]
            ])

            organism.update(input_enemy[:2] + input_food[:2])

        self.cull()

    def get_closest(self, organism, criteria, run):
        temp = list(filter(criteria, self.organisms))

        min_distance = -1
        min_index = -1

        eat_distance_sq = (organism.head_s / 2) ** 2

        angle = 0
        a2 = 0
        d2 = 0
        distance = ENV_MAX_DISTANCE_SQ

        for index, candidate in enumerate(temp):
            dist = (candidate.pos[0]-organism.pos[0])**2+(candidate.pos[1]-organism.pos[1])**2
            if min_distance == -1 or dist < min_distance:
                min_distance = dist
                min_index = index

        if min_index != -1:
            angle = ((atan2(
                temp[min_index].pos[1] - organism.pos[1],
                temp[min_index].pos[0] - organism.pos[0]
            ) - (organism.orientation)) % (2 * pi)) / pi

            a2 = atan2(
                temp[min_index].pos[1] - organism.pos[1],
                temp[min_index].pos[0] - organism.pos[0]
            )

            if min_distance < eat_distance_sq:
                run(organism, self.organisms[self.organisms.index(temp[min_index])])

            d2 = min_distance

            distance = d2 / ENV_MAX_DISTANCE_SQ


        return [distance, angle, d2, a2]

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

            for line in LINES_DEBUG:
                self.canvas.create_line(line[0][0], line[0][1], line[0][2], line[0][3], fill = "green")
                self.canvas.create_line(line[1][0], line[1][1], line[1][2], line[1][3], fill = "red")

        self.window.update_idletasks()
        self.window.update()
