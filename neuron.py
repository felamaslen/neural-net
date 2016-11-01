from math import e

def sigma(z):
    return 1 / (1 + pow(e, -max(-700, z)))

class Neuron(object):
    def __init__(self, weight, bias, num_inputs):
        self.weight = weight

        self.bias = bias

    def output(self, x):
        return sigma(sum(self.weight[i] * x[i] for i in range(len(self.weight))) + self.bias)


