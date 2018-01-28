class Node:

    def __init__(self, name):
        self.name = name
        self.node_type = "root"
        self.children = []
        self.parents = []

    def add_child(self, node):
        self.children.append(node)

    def add_parent(self, node):
        self.parents.append(node)
        
    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return "%s %s (%d children)".format(self.name, self.type, len(self.children))
