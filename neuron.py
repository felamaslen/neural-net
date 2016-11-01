from math import e

class Neuron(object):
    def __init__(self, weight, bias):
        self.apply_weight(weight)

        self.bias = bias

    @staticmethod
    def sigma(z):
        return 1 / (1 + pow(e, -max(-700, z)))


    def apply_weight(self, weight):
        """ apply normalised weights """
        total_weight = sum([abs(this_weight) for this_weight in weight])

        self.weight = [this_weight / total_weight for this_weight in weight]

    def output(self, x):
        """ weights should be normalised """
        return self.sigma(sum(self.weight[i] * x[i] for i in range(len(self.weight))) + self.bias)


