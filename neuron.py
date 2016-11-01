from math import e
import numpy as np

class Neuron(object):
    def __init__(self, weight, bias):
        self.weight = weight
        self.bias = bias

    @staticmethod
    def sigma(z):
        #return 1 / (1 + pow(e, -max(-700, z)))
        return 1 / (1 + np.exp(-z))

    def output(self, x):
        return self.sigma(np.dot(self.weight, x) + self.bias)


