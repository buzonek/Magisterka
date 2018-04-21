from functools import total_ordering


@total_ordering
class NeuralBaseClass(object):
    def __init__(self, value):
        self.value = value
        self.connections = {}

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value

    def connect(self, neuron):
        self.connections[neuron.value] = neuron
        neuron.connections[self.value] = self


class ValueNeuron(NeuralBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.sensor = None
        self.prev = None
        self.next = None

    def __repr__(self):
        return "ValueNeuron({0})".format(self.value, self.connections)


class ObjectNeuron(NeuralBaseClass):
    def __repr__(self):
        return "ObjectNeuron({0})".format(self.value)
