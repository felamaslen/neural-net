from math import pi

ENV_WIDTH = 1024
ENV_HEIGHT = 768

ENV_MAX_DISTANCE_SQ = ENV_WIDTH ** 2 + ENV_HEIGHT ** 2

VISUALISE = True

ENV_MAX_ORGANISMS = 30

SPAWN_FREQUENCY = 5

ORGANISM_BRAIN = [5,5,3]
ORGANISM_HEADSIZE = 5
ORGANISM_TAILSIZE = 16
ORGANISM_LEGSIZE = 6

ORGANISM_TURN_AMOUNT = pi / 16
ORGANISM_SPEED = 2

ORGANISM_SOFT_MAX_HEAD_SIZE = 30

PHOTOSYNTHESIS_RATE = 0.01
ORGANISM_INITIAL_SIZE = 100
ORGANISM_SIZE_LOSS = 0.0001
ORGANISM_SIZE_EFFICIENCY = 0.995

FEED_AMOUNT = 500

MINIMUM_SIZE = 4

MUTATION_RATE = 0.1

EAT_DISTANCE_SQ = 25

SLOW_DOWN = 0.002
