from Sensor import Sensor
from ValueNeuron import ValueNeuron


class AVBTreeNode(object):
    def __init__(self, is_leaf=True):
        self.keys = []
        self.childs = []
        self.parent = None
        self.leaf = is_leaf

    def __repr__(self):
        return "{0}".format(self.keys)

    def __len__(self):
        return len(self.keys)

    def get_key(self, value):
        for key in self.keys:
            if key.value == value:
                return key

    def add_key(self, AVBTree, obj, split=False):
        if not hasattr(obj, 'value'):
            raise ValueError('AVBTree node has to contain value property!')
        # print("Inserting {0} to the tree...".format(obj))
        index = 0
        length = len(self.keys)
        while index < length and self.keys[index].value < obj.value:
            index += 1

        if split:
            self.keys.insert(index, obj)

            # if node is full split it
            if self.is_full:
                self.split(AVBTree)
            return

        # this is a part responsible for creating connections
        if type(obj.value) in [int, float]:
            old_range = AVBTree.range
            # print("Old range is:", old_range)
            if length == 2:
                if index == 0:
                    obj.next = self.keys[0]
                    obj.prev = self.keys[0].prev
                    if self.keys[0].prev:
                        self.keys[0].prev.next = obj
                    self.keys[0].prev = obj
                elif index == 1:
                    obj.next = self.keys[1]
                    obj.prev = self.keys[0]
                    self.keys[1].prev = obj
                    self.keys[0].next = obj
                else:
                    obj.next = self.keys[1].next
                    obj.prev = self.keys[1]
                    if self.keys[1].next:
                        self.keys[1].next.prev = obj
                    self.keys[1].next = obj
            elif length == 1:
                if index == 0:
                    obj.next = self.keys[0]
                    obj.prev = self.keys[0].prev
                    if self.keys[0].prev:
                        self.keys[0].prev.next = obj
                    self.keys[0].prev = obj

                elif index == 1:
                    obj.next = self.keys[0].next
                    obj.prev = self.keys[0]
                    if self.keys[0].next:
                        self.keys[0].next.prev = obj
                    self.keys[0].next = obj

            else:
                obj.prev = AVBTree.min
                AVBTree.min.next = obj
                obj.next = AVBTree.max
                AVBTree.max.prev = obj

            # obj.next.calc_weights(AVBTree.range)
            # obj.prev.calc_weights(AVBTree.range)
            new_range = AVBTree.range
            # print("New range is:", new_range)
            # range_updated = new_range == old_range
            obj.calc_weights(new_range, new_range != old_range)
        self.keys.insert(index, obj)

        # if node is full split it
        if self.is_full:
            self.split(AVBTree)

    def add_child(self, child):
        i = 0
        length = len(self.childs)
        while i < length and self.childs[i].keys[0] < child.keys[0]:
            i += 1
        self.childs.insert(i, child)

    def split(self, AVBTree):
        rightmost_key = self.keys.pop()
        new_leaf = AVBTreeNode()
        new_leaf.add_key(AVBTree, rightmost_key, split=True)

        if self.childs:
            new_leaf.childs = self.childs[2:]
            for child in new_leaf.childs:
                child.parent = new_leaf
            self.childs = self.childs[:2]
            for child in self.childs:
                child.parent = self
            new_leaf.leaf = False

        middle_key = self.keys.pop()

        if self.parent:
            self.parent.add_child(new_leaf)
            new_leaf.parent = self.parent
            self.parent.add_key(AVBTree, middle_key, split=True)
        else:
            new_root = AVBTreeNode(is_leaf=False)
            new_root.add_key(AVBTree, middle_key, split=True)
            self.parent = new_root
            new_leaf.parent = new_root
            self.parent.add_child(self)
            self.parent.add_child(new_leaf)
            AVBTree.root = new_root

    @property
    def is_full(self):
        return len(self.keys) > 2

    @property
    def leftmost(self):
        return min(self.keys)

    @property
    def rightmost(self):
        return max(self.keys)

    def get_left_child(self):
        return self.childs[0]

    def get_middle_child(self):
        return self.childs[1]

    def get_right_child(self):
        right_child = self.childs[-1]
        return right_child


class AVBTree(object):
    def __init__(self, param=""):
        self.root = AVBTreeNode()
        self.param = param
        self.min = Sensor("Min")
        self.max = Sensor("Max")
        self.min.value_neuron = ValueNeuron("Min")
        self.max.value_neuron = ValueNeuron("Max")

    @property
    def range(self):
        if self.max.prev and self.min.next:
            return self.max.prev.value - self.min.next.value
        else:
            return 100000000

    @property
    def is_numerical(self):
        return type(self.root.keys[0].value) in [int, float]

    @property
    def param_range(self):
        if self.max.prev and self.min.next:
            range = self.max.prev.value - self.min.next.value
            return range
        else:
            return 10000000000

    def insert(self, obj):
        if obj.value is None:
            return None

        current_node = self.root

        # if key is present in that leaf increment counter
        while not current_node.leaf:
            key = current_node.get_key(obj.value)
            if key:
                key.count += 1
                return key
            if obj.value < current_node.leftmost.value:
                current_node = current_node.get_left_child()
            elif obj.value > current_node.rightmost.value:
                current_node = current_node.get_right_child()
            else:
                current_node = current_node.childs[1]

        # if key is present in that leaf increment counter
        key = current_node.get_key(obj.value)
        if key:
            key.count += 1
            return key

        # if no, add key to that leaf
        current_node.add_key(self, obj)
        obj.value_neuron = ValueNeuron(obj.value)
        obj.value_neuron.sensor = obj
        return obj

    def search(self, value):
        current_node = self.root
        while not current_node.leaf:
            key = current_node.get_key(value)
            if key:
                return key
            if value < current_node.leftmost.value:
                current_node = current_node.get_left_child()
            elif value > current_node.rightmost.value:
                current_node = current_node.get_right_child()
            else:
                current_node = current_node.childs[1]

        key = current_node.get_key(value)
        if not key:
            print("Value {0} not found!".format(value))
        return key

    def print_in_order(self):
        current_node = self.root
        while not current_node.leaf:
            current_node = current_node.get_left_child()
        current = self.min
        output = "In order: "
        while current:
            output += str(current.value) + '\t'
            current = current.next
        print(output)

    def print(self):
        this_level = [self.root]
        while this_level:
            next_level = []
            output = ""
            for node in this_level:
                if node.childs:
                    next_level.extend(node.childs)
                output += str(node) + "\t\t\t"
            print(output)
            this_level = next_level
        if hasattr(self, 'min'):
            self.print_in_order()
            print("Min: {0}, Max: {1}".format(self.min.next, self.max.prev))
