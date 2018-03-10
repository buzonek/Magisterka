from recordclass import recordclass


Key = recordclass('Key', 'value count')


class AVBTreeNode(object):
    def __init__(self, leaf=True):
        self.keys = []
        self.childs = []
        self.parent = None
        self.leaf = leaf

    def __repr__(self):
        return "{0}\tLeaf:{1}".format(self.keys, self.leaf)

    def add_key(self, AVBTree, k, count=1):
        self.keys.append(Key(value=k, count=count))
        self.keys.sort(key=lambda x: x.value)

        # if leaf is full split it
        if self.is_full:
            self.split(AVBTree)

    def split(self, AVBTree):

        rightmost_key = self.keys.pop()
        new_leaf = AVBTreeNode()
        new_leaf.add_key(AVBTree, rightmost_key.value, rightmost_key.count)
        if self.childs:
            new_leaf.childs = self.childs[1:]
            self.childs = self.childs[:1]
            new_leaf.leaf = False

        middle_key = self.keys.pop()

        if self.parent:
            self.parent.add_key(AVBTree, middle_key.value, middle_key.count)
            self.parent.childs.append(new_leaf)
        else:
            new_root = AVBTreeNode(leaf=False)
            new_root.add_key(AVBTree, middle_key.value, middle_key.count)
            self.parent = new_root
            new_leaf.parent = new_root
            self.parent.childs.append(self)
            self.parent.childs.append(new_leaf)
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
        right_child = self.childs[2] if len(self.childs) == 3 else self.childs[1]
        return right_child


class AVBTree(object):
    def __init__(self):
        self.root = AVBTreeNode()
        self.current_node = self.root

    def insert(self, value):
        self.current_node = self.root

        # if key is present in that leaf increment counter
        for key in self.current_node.keys:
            if key.value == value:
                key.count += 1
                break
        else:
            while not self.current_node.leaf:
                if value < self.current_node.leftmost:
                    self.current_node = self.current_node.get_left_child()
                elif value > self.current_node.rightmost:
                    self.current_node = self.current_node.get_right_child()
                else:
                    self.current_node = self.current_node.childs[1]

            # if key is present in that leaf increment counter
            for key in self.current_node.keys:
                if key.value == value:
                    key.count += 1
                    break
            # if no, add key to that leaf
            else:
                self.current_node.add_key(self, value)

    def search(self):
        pass

    def delete(self):
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
