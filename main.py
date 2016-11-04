#!/usr/bin/python3

from environment import Environment
from tkinter import *

import constants

class Simulation(object):
    def __init__(self):
        self.initialise_gui()
        self.run()
        while True:
            self.update()

    def initialise_gui(self):
        self.window = Tk()
        self.window.title("Neural Network Reinforcement Learning Simulation")

        self.canvas = Canvas(self.window)

        menubar = Menu(self.window)

        filemenu = Menu(menubar, tearoff=0)     
        menubar.add_cascade(label="File", menu=filemenu)

        editmenu = Menu(menubar, tearoff=0)     
        menubar.add_cascade(label="Edit", menu=editmenu)

        debugmenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Debug", menu=debugmenu)
        debugmenu.add_checkbutton(label="Hide Display", onvalue=True, offvalue=False, command = self.toggle_visualise)

        simulationmenu = Menu(filemenu, tearoff=0)
        organismmenu = Menu(filemenu, tearoff=0)

        filemenu.add_cascade(label="Simulation", menu=simulationmenu)
        simulationmenu.add_command(label="New", command=self.run)
        simulationmenu.add_command(label="Save", command=self.window.quit)
        simulationmenu.add_command(label="Load", command=self.window.quit)

        filemenu.add_cascade(label="Organism", menu=organismmenu)
        organismmenu.add_command(label="Save", command=self.window.quit)
        organismmenu.add_command(label="Load", command=self.window.quit)

        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.window.destroy)






        self.window.config(menu=menubar)

    def update(self):
        self.env.run_loop()
        self.window.update_idletasks()
        self.window.update()

    def run(self):
        self.canvas.pack()
        self.canvas.config(width=constants.ENV_WIDTH, height=constants.ENV_HEIGHT)
        self.env = Environment(self.canvas)

    def toggle_visualise(self): constants.VISUALISE = not constants.VISUALISE

sim = Simulation()