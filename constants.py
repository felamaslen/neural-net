from math import pi

SIMULATION_SPEED = 0.01 # seconds
CULL_PERIOD = 300
VISUALISE = True

ENV_WIDTH = 500
ENV_HEIGHT = 500

ORGANISM_GEN_RATE = 0.8

MUTATION_RATE = 0.05

CLONE_NUM = 5

""" initial number of organisms """
ENV_NUM_PLANTS = 20

""" initial size of organisms """
SIZE_PLANT = 5

""" initial hunger of organisms """
INITIAL_HUNGER = 0
MAX_HUNGER = 500

""" growth rate constant """
GROWTH_RATE = 0.005

GROWTH_EFFICIENCY = 1#0.999

DIGESTION_EFFICIENCY = 1

""" fraction of organism's size which can be eaten by an organism at once """
STOMACH_SIZE = 1

ORGANISM_HEAD_SCALE     = 1
ORGANISM_HEAD_COLOR     = "red"
ORGANISM_BODY_LENGTH    = 15
ORGANISM_BODY_COLOR     = "black"

THE_BRAIN = [2,2,2,2]

THRESHOLD_OUTPUT = 0.75

ORGANISM_MOVE_SPEED = 2
ORGANISM_MOVE_ANGLE = pi / 8

NUM_CHILDREN = 1
