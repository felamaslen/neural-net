from math import pi

SIMULATION_SPEED = 0#.05 # seconds
CULL_PERIOD = 300
VISUALISE = True

ENV_WIDTH = 500
ENV_HEIGHT = 500

ORGANISM_GEN_RATE = 0.1

MUTATION_RATE = 0.05

CLONE_NUM = 5

""" initial number of organisms """
ENV_NUM_PLANTS = 20

""" initial size of organisms """
SIZE_PLANT = 1

""" initial energy of organisms """
INITIAL_ENERGY = 1

""" energy usage rate constant """
ENERGY_USAGE_RATE = 0.01
ENERGY_SPEED_USAGE = 0.001

""" growth rate constant """
GROWTH_RATE = 1

""" a measure of how big we want organisms to get to """
MAX_SIZE = 10

""" rate of photosynthesis """
PHOTOSYNTHESIS_RATE = 0.01

""" how much energy is wasted when organisms are eaten """
DIGESTION_EFFICIENCY = 0.9

""" fraction of organism's size which can be eaten by an organism at once """
STOMACH_SIZE = 0.5

ORGANISM_HEAD_SCALE     = 2
ORGANISM_HEAD_COLOR     = "red"
ORGANISM_BODY_LENGTH    = 100
ORGANISM_BODY_COLOR     = "black"

THE_BRAIN = [3,10,30,20,3]

THRESHOLD_OUTPUT = 0.75

ORGANISM_MOVE_SPEED = 2
ORGANISM_MOVE_ANGLE = pi / 8

NUM_CHILDREN = 1
