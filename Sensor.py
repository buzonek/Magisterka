from ValueNeuron import NeuralBaseClass


class Sensor(NeuralBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.count = 1
        self.value_neuron = None
        self.prev = None
        self.next = None

    def __repr__(self):
        return "Sensor({0} -> {1} -> {2})".format(self.value, self.value_neuron, self.value_neuron.connections.keys())

