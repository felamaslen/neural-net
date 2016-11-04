from random import random
import numpy as np

class Neuron(object):
    def __init__(self, weights, bias, activation_func):
        self.weights = weights
        self.bias = bias
        self.activation_func = activation_func

    @staticmethod
    def Always(z):
        return True

    @staticmethod
    def Perceptron(z):
        return z>0

    @staticmethod
    def Sigmoid(z):
        return 1.0/(1.0+np.exp(-z))

    def get_output(self, inp):
        return self.activation_func(np.dot(self.weights,inp) + self.bias)


class ANN(object):
    def __init__(self, sizes, neurontype = None):
        self.layers = len(sizes)
        self.sizes = sizes
        self.neurontype = neurontype
        self.neurons = [[Neuron([0]*self.sizes[i-1], 0, neurontype) for j in range(self.sizes[i])] for i in range(1, self.layers)]

    def seed_network(self):
        for o in range(self.layers-1):                                          #for each layer of neurons
            for m in range(self.sizes[o+1]):                                    #for each neuron in the layer
                self.seed_neuron(o, m)

    def seed_neuron(self, layer, index, weightindex = 0):
        self.neurons[layer][index].weights = [random() - 0.5 for i in range(self.sizes[layer])]
        self.neurons[layer][index].bias = random() - 0.5

    def run(self, inputs):
        prev_outputs = np.array(inputs)
        for k in range(self.layers-1):
            prev_outputs = np.array([self.neurons[k][l].get_output(prev_outputs) for l in range(self.sizes[k+1])])
        return prev_outputs