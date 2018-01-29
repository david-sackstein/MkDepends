class Node:

    def __init__(self, name):
        self.name = name
        self.node_type = "unknown"
        self.children = []
        self.parents = []

    def set_type(self, node_type):
        self.node_type = node_type

    def add_child(self, node):
        self.children.append(node)

    def add_parent(self, node):
        self.parents.append(node)
        
    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return "%s %s (%d children) (%d parents)" % (self.name, self.node_type, len(self.children), len(self.parents))
