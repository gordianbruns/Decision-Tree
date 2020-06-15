class Tree:
    def __init__(self, root):
        self.root = root

    def get_root(self):
        return self.root


class Node:
    def __init__(self, value):
        self.value = value
        self.attributes = list()
        self.parent_value = None
        self.parent = None
        self.depth = 0

    def add_child(self, node, attribute):
        self.attributes.insert(0, (attribute, node))
        node.parent_value = attribute
        node.parent = self

    def get_value(self):
        return self.value

    def get_attributes(self):
        return self.attributes

    def insert_attribute(self, attribute):
        self.attributes.insert(0, attribute)

    def get_depth(self):
        return self.depth

    def set_depth(self, depth):
        self.depth = depth

    def get_parent(self):
        return self.parent

    def get_attributes(self):
        return self.attributes

    def print_tree(self):       # prints a tree in pre-order
        count = 0
        string = ""
        if self is None:
            return
        stack = list()
        stack.append((None, self))
        while len(stack) > 0:
            node = stack.pop()
            if node[1].depth == 1:
                string = node[1].parent.value + " = " + node[0]
            elif node[1].depth > 1 or node[1].value == "yes" or node[1].value == "no":
                string = "|" + 2 * node[1].parent.depth * " " + node[1].parent.value + " = " + node[1].parent_value
            if node[1].value == "yes":
                string += ": yes"
            elif node[1].value == "no":
                string += ": no"
            print(string)
            for attribute in node[1].attributes:
                stack.append(attribute)
                count += 1
        print("count =", count)
