import pydot

class GraphPlotter:

     def create_image(self, image_name, nodes):

        graph = pydot.Dot(graph_type='digraph')
        pydot_node_map = {}

        for node in nodes:
            color = self._get_color(node.node_type)
            pydot_node = pydot.Node(node.name + "(" + node.node_type + ")", style="filled", fillcolor=color)
            graph.add_node(pydot_node)
            pydot_node_map[node] = pydot_node

        for node in nodes:

            for child in node.children:
                if child not in pydot_node_map:
                    print()
                pydot_edge = pydot.Edge(pydot_node_map[node], pydot_node_map[child], label="depends on")
                graph.add_edge(pydot_edge)

        graph.write_svg(image_name)

        print(image_name)

     @staticmethod
     def _get_color(node_type):
        return "white" if node_type == "root" else "green" if node_type == "static" else "pink"
