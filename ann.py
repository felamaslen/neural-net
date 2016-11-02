#!/usr/bin/python3

import numpy as np
import pickle

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

    def seed_network(self):
        for o in range(self.layers-1):                                          #for each layer of neurons
            for m in range(self.sizes[o+1]):                                    #for each neuron in the layer
                self.seed_neuron(o, m)

    def seed_neuron(self, layer, index, weightindex = 0):
        self.neurons[layer][index].weights = np.random.randn(self.sizes[layer])
        self.neurons[layer][index].bias = np.random.randn()

    def run(self, inputs):
        prev_outputs = np.array(inputs)
        for k in range(self.layers-1):
            prev_outputs = np.array([self.neurons[k][l].get_output(prev_outputs) for l in range(self.sizes[k+1])])
        return prev_outputs