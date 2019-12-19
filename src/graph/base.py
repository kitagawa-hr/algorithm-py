from abc import ABCMeta, abstractmethod

from typing import List


class Vertex:
    __slots__ = ("data", "edges")

    def __init__(self, data=None):
        self.data = data
        self.edges = []

    def add_edge(self, to, weight=None) -> bool:
        for edge in self.edges:
            if edge.to == to:
                return False
        self.edges.append(Edge(to, weight))
        return True

    def remove_edge(self, to: int) -> bool:
        for i, edge in enumerate(self.edges):
            if edge.to == to:
                del self.edges[i]
                return True
        return False


class Edge:
    __slots__ = ("to", "weight")

    def __init__(self, to, weight=None):
        self.to = to
        self.weight = weight


class Graph(metaclass=ABCMeta):
    size: int

    @abstractmethod
    def get_weight(self, from_: int, to: int):
        pass

    @abstractmethod
    def edges_from(self, from_: int) -> "List[Edge]":
        pass

    @abstractmethod
    def add_edge(self, from_: int, to: int, weight=None) -> bool:
        pass

    @abstractmethod
    def remove_edge(self, from_: int, to: int) -> bool:
        pass

    @abstractmethod
    def is_adjacent(self, from_: int, to: int) -> bool:
        pass


class AdjacentListGraph(Graph):
    def __init__(self, vertices):
        self.vertices = vertices
        self.size = len(vertices)

    def get_weight(self, from_: int, to: int):
        for edge in self.vertices[from_].edges:
            if edge.to == to:
                return edge.weight
        return None

    def edges_from(self, from_: int):
        return self.vertices[from_].edges

    def add_edge(self, from_: int, to: int, weight=None) -> bool:
        return self.vertices[from_].add_edge(to, weight)

    def remove_edge(self, from_: int, to: int) -> bool:
        return self.vertices[from_].remove_edge(to)

    def is_adjacent(self, from_: int, to: int) -> bool:
        return to in {edge.to for edge in self.edges_from(from_)}


class AdjacentMatrixGraph(Graph):
    def __init__(self, size):
        self.size = size
        self.matrix = [[None for _ in range(size)] for _ in range(size)]

    def get_weight(self, from_: int, to: int):
        return self.matrix[from_][to]

    def edges_from(self, from_: int):
        return [
            Edge(i, weight)
            for i, weight in enumerate(self.matrix[from_])
            if weight is not None
        ]

    def add_edge(self, from_: int, to: int, weight=None) -> bool:
        if self.matrix[from_][to] is None:
            self.matrix[from_][to] = weight
            return True
        return False

    def remove_edge(self, from_: int, to: int) -> bool:
        if from_ >= self.size or to >= self.size:
            return False
        if self.matrix[from_][to] is not None:
            self.matrix[from_][to] = None
            return True
        return False

    def is_adjacent(self, from_: int, to: int) -> bool:
        return self.matrix[from_][to] is not None
