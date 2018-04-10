from ValueNeuron import NeuralBaseClass


class Sensor(NeuralBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.count = 1
        self.value_neuron = None

    def __repr__(self):
        return "Sensor({0})".format(self.value)

