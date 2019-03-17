from ValueNeuron import NeuralBaseClass
# from recordclass import recordclass
# Connection = recordclass('Connection', 'object count')


class Sensor(NeuralBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.count = 1
        self.value_neuron = None
        self.prev = None
        self.next = None
        self.weight_prev = 0
        self.weight_next = 0

        @property
        def next(self):
            return self.__next

        @next.setter
        def next(self, _next):
            print("Tutaj")
            self.next = _next
            self.value_neuron.next = _next.value_neuron

        @property
        def prev(self):
            return self.__prev

        @prev.setter
        def prev(self, _prev):
            # print("Tutaj")
            self.prev = _prev
            self.value_neuron.prev = _prev.value_neuron

    def calc_weights(self, value_range, range_updated=False):
        print("Calculating weights for", self)
        if self.value in ['Max', 'Min']:
            return

        if self.next and self.next.value != 'Max':
            self.weight_next = 1 - abs(self.next.value - self.value) / value_range
            self.next.weight_prev = self.weight_next
            print("Calculating next weight for {0}  {5}, range is {1}. {3} - {2} = {4}".format(self, value_range, self.value, self.next.value, self.weight_next, self.next))

        if self.prev and self.prev.value != 'Min':
            self.weight_prev = 1 - abs(self.prev.value - self.value) / value_range
            self.prev.weight_next = self.weight_prev

            print("Range has been updated, escalating to calculate weights of next ", self.next)
            if self.next.prev == self:
                print("Objects are the same!")
                return
            self.next.calc_weights(value_range, range_updated)
            if self.prev.next == self:
                print("Objects are the same!")
                return
            print("Range has been updated, escalating to calculate weights of prev ", self.prev)
            self.prev.calc_weights(value_range, range_updated)

    def __repr__(self):
        # return "Sensor({0} -> {1} -> {2})".format(self.value, self.value_neuron, self.value_neuron.connections.keys())
        return "{0}".format(self.value, self.weight_next)

        # return "Sensor([{2}] {0} [{1}])".format(self.value, self.weight_next, self.weight_prev)

