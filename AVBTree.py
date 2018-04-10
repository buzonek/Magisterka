from recordclass import recordclass
from Sensor import Sensor
import ctypes
# Key = recordclass('Key', 'value count')


class AVBTreeNode(object):
    def __init__(self, leaf=True):
        self.keys = []
        self.childs = []
        self.parent = None
        self.leaf = leaf

    def __repr__(self):
        return "{0}".format(self.keys)

    def get_key(self, value):
        for key in self.keys:
            if key.value == value:
                return key

    def add_key(self, AVBTree, obj):
        i = 0
        length = len(self.keys)
        while i < length and self.keys[i].value < obj.value:
            i += 1
        self.keys.insert(i, obj)

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
        new_leaf.add_key(AVBTree, rightmost_key)

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
            self.parent.add_key(AVBTree, middle_key)
        else:
            new_root = AVBTreeNode(leaf=False)
            new_root.add_key(AVBTree, middle_key)
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
        return min([key.value for key in self.keys])

    @property
    def rightmost(self):
        return max([key.value for key in self.keys])

    def get_left_child(self):
        return self.childs[0]

    def get_right_child(self):
        right_child = self.childs[-1]
        return right_child


class AVBTree(object):
    def __init__(self, param=""):
        self.root = AVBTreeNode()
        self.param = param

    def insert(self, obj):
        if obj.value is None:
            return
        current_node = self.root

        # if key is present in that leaf increment counter
        while not current_node.leaf:
            key = current_node.get_key(obj.value)
            if key:
                key.count += 1
                return key
            if obj.value < current_node.leftmost:
                current_node = current_node.get_left_child()
            elif obj.value > current_node.rightmost:
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
        return obj

    def search(self, value):
        current_node = self.root
        while not current_node.leaf:
            key = current_node.get_key(value)
            if key:
                return key
            if value < current_node.leftmost:
                current_node = current_node.get_left_child()
            elif value > current_node.rightmost:
                current_node = current_node.get_right_child()
            else:
                current_node = current_node.childs[1]

        key = current_node.get_key(value)
        if not key:
            print("Value {0} not found!".format(value))
        return key

    def traverse(self):
        pass

    def print(self):
        """Print an level-order representation."""
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
