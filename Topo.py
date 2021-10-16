from Structures import *


class Topo:
    _nodes = []
    _edges = []

    def get_edge_by_id(self, edge_no) -> Edge:
        return self._edges[edge_no] if edge_no < len(self._edges) else None

    def get_node_by_id(self, node_no) -> Node:
        return self._nodes[node_no] if node_no < len(self._nodes) else None

    def add_edge(self, edge: Edge):
        edge.no = len(self._edges)
        self._edges.append(edge)

    def add_node(self, node: Node):
        node.no = len(self._nodes)
        self._nodes.append(node)
