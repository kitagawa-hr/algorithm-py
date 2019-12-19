import unittest

from src.graph import base


class TestAdjacentListGraph(unittest.TestCase):
    def prepare_graph(self, graph):
        """
        0 ---> 1
        |   /  | ^
        |  /   |  2
        v v    v v
        4 <---  3
        """
        graph.add_edge(0, 1, 1)
        graph.add_edge(0, 4, 4)
        graph.add_edge(1, 3, 2)
        graph.add_edge(1, 4, 3)
        graph.add_edge(2, 1, 1)
        graph.add_edge(2, 3, 1)
        graph.add_edge(3, 4, 1)
        return graph

    def setUp(self):
        self.list_graph = self.prepare_graph(
            base.AdjacentListGraph([base.Vertex() for _ in range(5)])
        )
        self.matrix_graph = self.prepare_graph(base.AdjacentMatrixGraph(5))
        self.graphs = (self.list_graph, self.matrix_graph)

    def test_edges_from(self):
        test_cases = [(0, [1, 4]), (1, [3, 4]), (2, [1, 3]), (3, [4]), (4, [])]
        for graph in self.graphs:
            for from_, to_edges in test_cases:
                for expected, actual in zip(to_edges, graph.edges_from(from_)):
                    self.assertEqual(expected, actual.to)

    def test_get_weight(self):
        test_cases = [
            (0, 1, 1),
            (0, 4, 4),
            (2, 3, 1),
            (1, 2, None),
            (0, 2, None),
            (0, 3, None),
            (2, 4, None),
            (2, 0, None),
        ]
        for graph in self.graphs:
            for from_, to, weight in test_cases:
                self.assertEqual(weight, graph.get_weight(from_, to))

    def test_is_adjacent(self):
        test_cases = [
            (0, 1, True),
            (0, 4, True),
            (2, 3, True),
            (1, 2, False),
            (0, 2, False),
            (0, 3, False),
            (2, 4, False),
            (2, 0, False),
        ]
        for graph in self.graphs:
            for from_, to, is_adjacent in test_cases:
                self.assertEqual(is_adjacent, graph.is_adjacent(from_, to))

    def test_remove_edge(self):
        """
        0 ---> 1
            / |
            /  |  2
            v   v v
        4 <--- 3
        """
        for graph in self.graphs:
            self.assertEqual(True, graph.remove_edge(0, 4))
            self.assertEqual(False, graph.remove_edge(0, 4))
            self.assertEqual(True, graph.remove_edge(2, 1))
            self.assertEqual(False, graph.remove_edge(1, 5))
            test_cases = [(0, [1]), (1, [3]), (2, [3]), (3, [4]), (4, [])]
            for from_, to_edges in test_cases:
                for expected, actual in zip(to_edges, graph.edges_from(from_)):
                    self.assertEqual(expected, actual.to)
