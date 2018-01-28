import operator

from Edge import Edge
from Node import Node


class TreeBuilder:

    def __init__(self, android_mks):
        self.android_mks = android_mks

    def build(self):

        node_map = {}
        root_nodes = []

        for module in self._iter_modules():

            name = module.name
            node = _find_or_add_node(name, node_map)
            root_nodes.append(node)

            for static_library in module.static_libraries:
                add_child(static_library, node, node_map, root_nodes)

            for shared_library in module.shared_libraries:
                add_child(shared_library, node, node_map, root_nodes)

        return root_nodes

    def find_dependencies_of(self, module_name):
        state = self._RecursionState(self.module_map)
        self._find_depended_on_by(module_name, "root", "root", state)
        state.print_cycles()
        return state.get_edges()

    def _find_node(self, root, node_name, tracked):
        if root in tracked:
            return None, False

        if root.name == node_name:
            return root, True

        tracked.append(root)

        for child in root.children:
            node, found = self._find_node(child, node_name, tracked)
            if found:
                return node, True

        tracked.remove(root)

        return None, False

    def _get_node_heights(self, root):
        node_height_map = {}
        tracked = []
        for node, height in self._deep_search_first(root, 0, tracked):
            if node in node_height_map:
                node_height_map[node] = max(node_height_map[node], height)
            else:
                node_height_map[node] = height
        return node_height_map

    def _deep_search_first(self, node, height, tracked):

        if node in tracked:
            return

        tracked.append(node)

        for child in node.children:
            yield from self._deep_search_first(child, height+1, tracked)

        tracked.remove(node)

        yield node, height

    def _find_depended_on_by(self, module_name, parent_module_name, edge_type, state):

        if state.is_tracked(module_name):
            _add_if_new(Edge(module_name, parent_module_name, edge_type), state.cycle_edge_map)
            return

        if not module_name in self.module_map:
            # a leaf that was not converted to a node by AndroidMkReader because it could not be expanded
            _add_if_new(Edge(module_name, parent_module_name, edge_type), state.edge_map)
            return

        module = self._get_module_from_name(module_name)

        # depth first

        state.push_tracked(module_name)

        self.recurse_find_depended_on_by(module, state)

        state.pop_tracked(module_name)

        # add edge to this module after recursion of depth

        edge = Edge(module_name, parent_module_name, edge_type)

        _add_if_new(edge, state.edge_map)

    def _get_module_from_name(self, module_name):
        mk = self.module_map[module_name]
        return mk.modules.get(module_name)

    def recurse_find_depended_on_by(self, module, state):
        for static_library in module.static_libraries:
            self._find_depended_on_by(static_library, module.name, "static", state)
        for shared_library in module.shared_libraries:
            self._find_depended_on_by(shared_library, module.name, "shared", state)

    def _iter_modules(self):
        for android_mk in self.android_mks:
            for module in android_mk.modules.values():
                yield module

    class _RecursionState:
        def __init__(self, module_map):
            self.module_map = module_map
            self.edge_map = {}
            self.cycle_edge_map = {}
            self.back_tracker = []

        def push_tracked(self, module_name):
            self.back_tracker.append(module_name)

        def pop_tracked(self, module_name):
            self.back_tracker.remove(module_name)

        def is_tracked(self, module_name):
            return module_name in self.back_tracker

        def print_cycles(self):
            for edge in self.cycle_edge_map.values():
                child_name = edge.child_name
                parent_name = edge.parent_name

                child_mk = self.module_map[child_name]
                parent_mk = self.module_map[parent_name]

                print("cycle caused by {0} depending on {1}".format(child_name, parent_name))
                print("\t{0} is in {1}".format(child_name, child_mk.path))
                print("\t{0} is in {1}".format(parent_name, parent_mk.path))

        def get_edges(self):
            return self.edge_map.values()


def _add_if_new(edge, edge_map):
    key = str(edge)
    if key not in edge_map:
        edge_map[key] = edge


def _create_module_map(android_mks):
    module_map = {}
    for mk in android_mks:
        for m in mk.modules.values():
            module_map[m.name] = mk
    return module_map

def _find_or_add_node(name, node_map):
    if name not in node_map:
        node_map[name] = Node(name)
    return node_map[name]

def add_child(child_name, parent_node, node_map, root_nodes):
    child_node = _find_or_add_node(child_name, node_map)
    child_node.add_parent(parent_node)
    parent_node.add_child(child_node)
    if child_node in root_nodes:
        root_nodes.remove(child_node)

