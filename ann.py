#!/usr/bin/python3

import numpy as np

class Neuron(object):
    def __init__(self, weights, bias):
        self.weights = weights
        self.bias = bias

    @staticmethod
    def activation_func(z):
        return True

    def get_output(self, inp):
        return self.activation_func(np.dot(self.weights,inp) + self.bias)

class Perceptron(Neuron):
    def __init__(self, weights, bias):
        super(Perceptron, self).__init__(weights, bias)

    @staticmethod
    def activation_func(z):
        return z>0

class Sigmoid(Neuron):
    def __init__(self, weights, bias):
        super(Sigmoid, self).__init__(weights, bias)

    @staticmethod
    def activation_func(z):
        return 1.0/(1.0+np.exp(-z))



class ANN(object):
    def __init__(self, sizes, neurontype = Sigmoid):
        self.layers = len(sizes)
        self.sizes = sizes
        self.neurontype = neurontype
        self.neurons = [[self.neurontype([0]*self.sizes[i-1], 0) for j in range(self.sizes[i])] for i in range(1, self.layers)]

    def rand_seed(self):
        for o in range(1, self.layers):
            for m in range(self.sizes[o]):
                self.neurons[o-1][m].weights = np.random.randn(self.sizes[o-1])
                self.neurons[o-1][m].bias = np.random.randn()

    def feed_forward(self, inputs):
        prev_outputs = np.array(inputs)
        for k in range(self.layers-1):
            prev_outputs = np.array([self.neurons[k][l].get_output(prev_outputs) for l in range(self.sizes[k+1])])
        return prev_outputs