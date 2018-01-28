import pydot

class GraphPlotter:

     def create_image(self, image_name, edge_list):

        graph = pydot.Dot(graph_type='digraph')

        pydot_node_map = {}

        for edge in edge_list:

            edge_type = edge.edge_type
            node_name = edge.child_name

            color = self._get_color(edge_type)

            pydot_node = pydot.Node(node_name + "(" + edge_type + ")", style="filled", fillcolor=color)
            graph.add_node(pydot_node)
            pydot_node_map[node_name] = pydot_node

        for edge in edge_list:

            if edge.parent_name in pydot_node_map:
                pydot_node = pydot_node_map[edge.child_name]
                parent_pydot_node = pydot_node_map[edge.parent_name]
                pydot_edge = pydot.Edge(parent_pydot_node, pydot_node, label="depends on")

                graph.add_edge(pydot_edge)

        graph.write_svg(image_name)

        print(image_name)

     @staticmethod
     def _get_color(edge_type):
        color = "white" if edge_type == "root" else "green" if edge_type == "static" else "pink"
        return color
