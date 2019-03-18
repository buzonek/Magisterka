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

    def calc_left_weight(self, value_range, range_updated):
        if self.prev and self.prev.value != 'Min':
            # print("Calculating prev weight for {0}  {5}, range is {1}. {3} - {2} = {4}".format(self, value_range, self.value, self.prev.value, self.weight_prev, self.prev))
            self.weight_prev = 1 - abs(self.prev.value - self.value) / value_range
            self.prev.weight_next = self.weight_prev
            if range_updated:
                # print("Range has been updated, going to calculate value of prev!")
                self.prev.calc_left_weight(value_range, range_updated)

    def calc_right_weight(self, value_range, range_updated):
        if self.next and self.next.value != 'Max':
            # print("Calculating next weight for {0}  {5}, range is {1}. {3} - {2} = {4}".format(self, value_range, self.value, self.next.value, self.weight_next, self.next))
            self.weight_next = 1 - abs(self.next.value - self.value) / value_range
            self.next.weight_prev = self.weight_next
            if range_updated:
                # print("Range has been updated, going to calculate value of next!")
                self.next.calc_right_weight(value_range, range_updated)

    def calc_weights(self, value_range, range_updated=False):
        # if sensor is either Max or Min then it's unnecessary to calc weights
        if self.value in ['Max', 'Min']:
            return

        # print("Calculating weights for", self)
        self.calc_right_weight(value_range, range_updated)
        self.calc_left_weight(value_range, range_updated)

    def __repr__(self):
        # return "Sensor({0} -> {1} -> {2})".format(self.value, self.value_neuron, self.value_neuron.connections.keys())
        return "[{2}] ,{0}, [{1}]".format(self.value, self.weight_next, self.weight_prev)

        # return "Sensor([{2}] {0} [{1}])".format(self.value, self.weight_next, self.weight_prev)

