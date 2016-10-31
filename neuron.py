def sigma(z):
    return 1 / (1 + pow(e, -z))

class Neuron(object):
    def __init__(self, weight, bias, num_inputs):
        self.bias = bias

    def output(self, x):
        return sigma(sum(weight * x[i] for (i, weight) in self.w) + self.bias)


