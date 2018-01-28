from Node import Node

class Edge:

    def __init__(self, child_name, parent_name, edge_type):
        self.child_name = child_name
        self.parent_name = parent_name
        self.edge_type = edge_type

    def __str__(self):
        return self.parent_name + " -> " + self.child_name

    def invert(self):
        return Edge(self.parent_name, self.child_name, self.edge_type)

    def __repr__(self):
        return str(self)