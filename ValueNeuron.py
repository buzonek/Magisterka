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


class ValueNeuron(NeuralBaseClass):
    def __init__(self, value):
        super().__init__(value)

    def __repr__(self):
        return "ValueNeuron({0})".format(self.value)


class IDNeuron(NeuralBaseClass):
    def __repr__(self):
        return "IDNeuron({0})".format(self.value)
