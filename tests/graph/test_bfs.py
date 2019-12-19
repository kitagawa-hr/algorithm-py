import unittest

from src.graph import base, bfs

class TestDFS(unittest.TestCase):
    def prepare_graph(self, graph):
        r"""
          1
         / \
        8   3
        |  /  \
        4 6    5
          |    / \
          2   7   9 - 0
        """
        graph.add_edge(1, 8, 1)
        graph.add_edge(8, 4, 1)
        graph.add_edge(1, 3, 1)
        graph.add_edge(3, 6, 1)
        graph.add_edge(3, 5, 1)
        graph.add_edge(5, 7, 1)
        graph.add_edge(5, 9, 1)
        graph.add_edge(6, 2, 1)
        graph.add_edge(9, 0, 1)
        return graph
    def setUp(self):
        self.list_graph = self.prepare_graph(base.AdjacentListGraph([base.Vertex() for _ in range(10)]))
        self.matrix_graph = self.prepare_graph(base.AdjacentMatrixGraph(10))
        self.graphs = (self.list_graph, self.matrix_graph)

    def test_distances_from(self):
        distances_from_one = [4, 0, 3, 1, 2, 2, 2, 3, 1, 3]
        for graph in self.graphs:
            self.assertEqual(distances_from_one, bfs.distances_from(graph, 1))

    def test_shortest_path(self):
        path = [1, 3, 5, 9, 0]
        for graph in self.graphs:
            self.assertEqual(path, bfs.shortest_path(graph, 1, 0))
