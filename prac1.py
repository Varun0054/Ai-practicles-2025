"""Depth-First Search (DFS) examples for an undirected graph.

This module provides:
- dfs_recursive(graph, start, visited=None, order=None): recursive DFS from a start node, returns visit order
- dfs_full(graph): runs DFS for all components and returns visit order covering every vertex

Graph representation: adjacency list as a dict where keys are nodes and values are lists of neighbors.

Simple demo and basic assertions are run when executed as a script.
"""

from typing import Dict, List, Set, Any


def dfs_recursive(graph: Dict[Any, List[Any]], start: Any, visited: Set[Any] = None, order: List[Any] = None) -> List[Any]:
	"""Perform a recursive depth-first search starting from `start`.

	Args:
		graph: adjacency list for an undirected graph (dict of node -> list of neighbors).
		start: starting node for this DFS call.
		visited: set used to track visited nodes (created if None).
		order: list used to record visitation order (created if None).

	Returns:
		The list of nodes visited in DFS order for the component containing `start`.
	"""
	if visited is None:
		visited = set()
	if order is None:
		order = []

	visited.add(start)
	order.append(start)

	for neighbor in graph.get(start, []):
		if neighbor not in visited:
			dfs_recursive(graph, neighbor, visited, order)

	return order


def dfs_full(graph: Dict[Any, List[Any]]) -> List[Any]:
	"""Run DFS so that every vertex in the graph is visited (covers disconnected graphs).

	Returns a list with the visitation order across all components. The order visits
	components in the iteration order of `graph.keys()`.
	"""
	visited: Set[Any] = set()
	order: List[Any] = []

	for node in graph:
		if node not in visited:
			# start a DFS for this component; pass visited and order to collect global state
			dfs_recursive(graph, node, visited, order)

	return order


def build_undirected_graph(edges: List[tuple]) -> Dict[Any, List[Any]]:
	"""Build an undirected adjacency list from an edge list.

	Example:
		edges = [('A','B'), ('A','C'), ('B','D')]
	"""
	g: Dict[Any, List[Any]] = {}
	for a, b in edges:
		g.setdefault(a, []).append(b)
		g.setdefault(b, []).append(a)
	return g


def _demo():
	# Example graph with two components (G is isolated)
	edges = [
		("A", "B"), ("A", "C"),
		("B", "D"), ("B", "E"),
		("C", "F"), ("E", "F"),
		# node G will be isolated, demonstrate disconnected graph handling
	]

	graph = build_undirected_graph(edges)
	graph.setdefault("G", [])

	print("Adjacency list:")
	for k in sorted(graph):
		print(f"  {k}: {graph[k]}")

	print("\nDFS from 'A' (component of A):")
	order_from_a = dfs_recursive(graph, "A")
	print(order_from_a)

	print("\nFull DFS covering all vertices:")
	full_order = dfs_full(graph)
	print(full_order)

	# Basic verification: full DFS should visit every node exactly once
	assert set(full_order) == set(graph.keys()), "DFS did not visit all vertices"
	assert len(full_order) == len(graph), "Visited count doesn't match vertex count"
	print("\nAssertions passed: all vertices visited.")


if __name__ == "__main__":
	_demo()

