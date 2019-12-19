from collections import deque
from typing import List

from .base import Graph


def distances_from(
    graph: "Graph", from_: int, break_if=lambda node: False
) -> "List[int]":
    distances = [None for _ in range(graph.size)]
    distances[from_] = 0
    queue = deque([from_])
    while queue:
        node = queue.popleft()
        if break_if(node):
            break
        curDist = distances[node]
        for edge in graph.edges_from(node):
            if distances[edge.to] is not None:
                continue
            delta = edge.weight if edge.weight else 0
            distances[edge.to] = curDist + delta
            queue.append(edge.to)
    return distances


def shortest_path(graph: "Graph", from_: int, to: int) -> "List[int]":
    before_nodes = [None for _ in range(graph.size)]
    queue = deque([from_])
    while queue:
        node = queue.popleft()
        if node == to:
            cur = to
            path = deque([cur])
            while cur != from_:
                cur = before_nodes[cur]
                path.appendleft(cur)
            return list(path)
        for edge in graph.edges_from(node):
            if before_nodes[edge.to] is not None:
                continue
            before_nodes[edge.to] = node
            queue.append(edge.to)
    return []
