import operator

from Node import Node

class TreeBuilder:

    def __init__(self, android_mks):
        self._android_mks = android_mks
        self._node_map = {}
        self._leaf_nodes = set()
        self._not_leaf_nodes = set()
        self._root_nodes = set()
        self._not_root_nodes = set()

    def build(self):

        for module in self._iter_modules():

            name = module.name
            parent_node = self._add_parent(module, name)

            for static_library in module.static_libraries:
                self.add_child(static_library, "static", parent_node)

            for shared_library in module.shared_libraries:
                self.add_child(shared_library, "shared", parent_node)

        self._root_nodes -= self._not_root_nodes
        self._leaf_nodes -= self._not_leaf_nodes

        return self._root_nodes, self._leaf_nodes

    def _add_parent(self, module, name):
        node = self._find_or_add_node(name)
        self._root_nodes.add(node)
        has_children = len(module.static_libraries) + len(module.shared_libraries) > 0
        if has_children:
            self._not_leaf_nodes.add(node)
        return node

    def add_child(self, child_name, node_type, parent_node):
        child_node = self._find_or_add_node(child_name)
        child_node.set_type(node_type)
        child_node.add_parent(parent_node)
        parent_node.add_child(child_node)
        self._leaf_nodes.add(child_node)
        self._not_root_nodes.add(child_node)

    def _find_or_add_node(self, name):
        if name not in self._node_map:
            self._node_map[name] = Node(name)
        return self._node_map[name]

    def iter_nodes_dfs(self, root_node):
        visited = set()

        return self.dfs(root_node, visited)

    # def dfs(self, node, visited):
    #     visited.add(node)
    #     for child in node.children:
    #         if child not in visited:
    #             yield from self.dfs(child, visited)
    #     yield node
    #
    # def is_cyclic(self):
    #
    #     visited = set()
    #     rec_stack = set()
    #
    #     def is_cyclic_util(node):
    #         visited.add(node)
    #         rec_stack.add(node)
    #
    #         for child in node.children:
    #             if child not in visited:
    #                 if self.is_cyclic_util(child):
    #                     return True
    #             elif rec_stack[child]:
    #                 return True
    #
    #         rec_stack.remove(node)
    #         return False
    #
    #     return False
    #
    #     for node in self._node_map:
    #         if node not in visited:
    #             if is_cyclic_util(node):
    #                 return True

    def _iter_modules(self):
        for android_mk in self._android_mks:
            for module in android_mk.modules.values():
                yield module

