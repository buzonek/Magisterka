from functools import total_ordering
from abc import ABCMeta


@total_ordering
class NeuralBaseClass(object):
    def __init__(self, value):
        self.value = value
        self.connections = {}

    def __lt__(self, other):
        return self.value < other.value

    # def __eq__(self, other):
    #     return self.value == other.value

    def connect(self, neuron):
        self.connections[neuron.value] = neuron
        neuron.connections[self.value] = self


class ValueNeuron(NeuralBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.sensor = None
        self.__prev = None
        self.__next = None
        self.weight_prev = 0
        self.weight_next = 0


    @property
    def next(self):
        return self.__next

    @next.setter
    def next(self, next_obj):
        self.next = next_obj
        self.weight_next = 1 - abs(self.next.value - self.value) / self.sensor

    @property
    def prev(self):
        return self.__prev

    @prev.setter
    def prev(self, prev_obj):
        # print("Tutaj")
        self.prev = prev_obj

    def calc_weights(self, range):
        print("kalkuluje")
        if self.__next:
            self.weight_next = 1 - abs(self.next.value - self.value) / range

        if self.__prev:
            self.weight_prev = 1 - abs(self.prev.value - self.value) / range

    def __repr__(self):
        return "ValueNeuron({0})".format(self.value, self.connections)


class ObjectNeuron(NeuralBaseClass):
    def __repr__(self):
        return "ObjectNeuron({0})".format(self.value)
