from math import e

class Neuron(object):
    def __init__(self, weight, bias):
        self.weight = weight
        self.bias = bias

    @staticmethod
    def sigma(z):
        return 1 / (1 + pow(e, -max(-700, z)))

    def output(self, x):
        return self.sigma(sum(self.weight[i] * x[i] for i in range(len(self.weight))) + self.bias)


