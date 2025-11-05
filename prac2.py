"""Breadth-First Search (BFS) examples for an undirected graph.

This module implements a recursive BFS (level-by-level recursion) and a
full-graph BFS that covers disconnected graphs.

Graph representation: adjacency list as a dict where keys are nodes and values are lists of neighbors.
"""

from typing import Dict, List, Set, Any


def bfs_recursive(graph: Dict[Any, List[Any]], start: Any) -> List[Any]:
	"""Perform a recursive breadth-first search starting from `start`.

	This implementation treats BFS as a level-order traversal. It uses recursion
	to process one "frontier" (level) at a time. It's a clear, recursive way to
	express BFS without explicit queue objects in the outer API.

	Args:
		graph: adjacency list for an undirected graph (dict of node -> list of neighbors).
		start: starting node for the BFS.

	Returns:
		A list of nodes in the order they were visited by BFS for the component containing `start`.
	"""
	visited: Set[Any] = set([start])
	order: List[Any] = [start]

	def _bfs_level(frontier: List[Any]):
		# gather neighbors for the next level
		next_level: List[Any] = []
		for node in frontier:
			for nbr in graph.get(node, []):
				if nbr not in visited:
					visited.add(nbr)
					order.append(nbr)
					next_level.append(nbr)
		if next_level:
			_bfs_level(next_level)

	_bfs_level([start])
	return order


def bfs_full(graph: Dict[Any, List[Any]]) -> List[Any]:
	"""Run BFS so that every vertex in the graph is visited (covers disconnected graphs).

	The order will start BFS from nodes in the iteration order of `graph.keys()`
	for any components that haven't been visited yet.
	"""
	visited: Set[Any] = set()
	order: List[Any] = []

	for node in graph:
		if node not in visited:
			# run a component BFS but share visited and order
			# small wrapper to reuse bfs_recursive logic while reusing visited/order
			visited.add(node)
			order.append(node)

			def _bfs_level(frontier: List[Any]):
				next_level: List[Any] = []
				for v in frontier:
					for nbr in graph.get(v, []):
						if nbr not in visited:
							visited.add(nbr)
							order.append(nbr)
							next_level.append(nbr)
				if next_level:
					_bfs_level(next_level)

			_bfs_level([node])

	return order


def build_undirected_graph(edges: List[tuple]) -> Dict[Any, List[Any]]:
	"""Build an undirected adjacency list from an edge list."""
	g: Dict[Any, List[Any]] = {}
	for a, b in edges:
		g.setdefault(a, []).append(b)
		g.setdefault(b, []).append(a)
	return g


def _demo():
	# Example graph with a cycle and an isolated node H
	edges = [
		("1", "2"), ("1", "3"),
		("2", "4"), ("2", "5"),
		("3", "6"), ("5", "6"),
		("6", "7"),
	]

	graph = build_undirected_graph(edges)
	graph.setdefault("H", [])  # isolated node to show disconnected coverage

	print("Adjacency list:")
	for k in sorted(graph):
		print(f"  {k}: {graph[k]}")

	print("\nBFS from '1' (component of 1):")
	order_from_1 = bfs_recursive(graph, "1")
	print(order_from_1)

	print("\nFull BFS covering all vertices:")
	full_order = bfs_full(graph)
	print(full_order)

	# Basic verification: full BFS should visit every node exactly once
	assert set(full_order) == set(graph.keys()), "BFS did not visit all vertices"
	assert len(full_order) == len(graph), "Visited count doesn't match vertex count"
	print("\nAssertions passed: all vertices visited by BFS.")


if __name__ == "__main__":
	_demo()

