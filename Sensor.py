# from AVBTree import AVBTree
#
#
# class SensoryInputField(object):
#     def __init__(self):
#         self.avb_tree = AVBTree()


class Sensor(object):
    def __init__(self, value):
        self.value = value
        self.count = 1
        self.connections = {}

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __repr__(self):
        return "<{0}|{1}>".format(self.value, self.count)

