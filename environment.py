import tkinter

from constants import *

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
        self.window.mainloop()

    def run_loop(self):
        self.organisms = []
        self.framecounter = 0
        while True:
            handle_organisms()

            if not self.framecounter%100:   #spawn a new organism every 100 frames
                self.spawn_organism()
            self.framecounter += 1

    def spawn_organism(self):
        self.organisms += Organism([random()*self.dims[0], random()*self.dims[1]] ,self.dims)

    def handle_organisms(self):
        for organism in self.organisms:
            organism.update(
                    self.get_closest(organism, lambda x: x.size < organism.size) +    #closest predator
                    self.get_closest(organism, lambda x: x.size > organism.size))     #closest prey

        cull()

    def get_closest(self, organism, function):
        temp = list(filter(function, self.organisms))
        temp.remove(organism)

        min_distance = -1
        min_index = -1

        for index, candidate in enumerate(temp):
            dist = (candidate.pos[0]-organism.pos[0])^2+(candidate.pos[1]-organism.pos[1])^2
            if min_distance == -1 or dist < min_distance:
                min_distance = dist
                min_index = index

        if min_index != -1:
            angle = atan2(
                temp[min_index].pos[0] - organism.pos[0],
                temp[min_index].pos[1] - organism.pos[1])

            return [min_distance ** 0.5, angle]

        return [0] * 2

    def cull(self):
        for organism in self.organisms:
            if organism.cull:
                self.organisms.remove(organism)


    def draw(self):
        self.canvas.delete(tkinter.ALL)

        if VISUALISE:
            for organism in self.organisms:
                organism.draw(self.canvas)

        self.window.update_idletasks()
        self.window.update()
