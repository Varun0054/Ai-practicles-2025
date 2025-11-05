"""Minimum Spanning Tree (MST) Implementation using Kruskal's Algorithm (Greedy Approach).

This module focuses on Kruskal's MST algorithm, a greedy approach that:
1. Sorts all edges by weight (greedy choice property)
2. Processes edges in ascending weight order
3. Includes each edge that doesn't create a cycle (using Union-Find)

The implementation includes:
- kruskal_mst(edges, nodes): Main MST algorithm using Union-Find
- Utility functions for graph representation
- Demo with a sample weighted undirected graph

Example usage:
    edges = [("A","B",4), ("B","C",8), ("A","C",5)]
    nodes = ["A","B","C"]
    mst_edges, total = kruskal_mst(edges, nodes)
"""

from typing import Dict, List, Tuple, Any
import heapq


def kruskal_mst(edges: List[Tuple[Any, Any, float]], nodes: List[Any]) -> Tuple[List[Tuple[Any, Any, float]], float]:
    """Kruskal's algorithm.

    Args:
        edges: list of (u, v, weight) for undirected edges.
        nodes: list of all nodes in the graph.

    Returns:
        A tuple (mst_edges, total_weight).
    """
    # Disjoint set (Union-Find)
    parent = {n: n for n in nodes}
    rank = {n: 0 for n in nodes}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry:
            return False
        if rank[rx] < rank[ry]:
            parent[rx] = ry
        else:
            parent[ry] = rx
            if rank[rx] == rank[ry]:
                rank[rx] += 1
        return True

    # sort edges by weight (greedy choice)
    sorted_edges = sorted(edges, key=lambda e: e[2])

    mst = []
    total = 0.0

    for u, v, w in sorted_edges:
        if union(u, v):
            mst.append((u, v, w))
            total += w
            if len(mst) == len(nodes) - 1:
                break

    return mst, total


def prim_mst(adj: Dict[Any, List[Tuple[Any, float]]], start: Any = None, visited: set = None) -> Tuple[List[Tuple[Any, Any, float]], float]:
    """Prim's algorithm for a single connected component.

    Args:
        adj: adjacency dict node -> list of (neighbor, weight).
        start: optional start node; if None use an arbitrary node from adj.
        visited: optional set of already visited nodes; if provided, the function
                 will add newly visited nodes to this set. This allows composing
                 a full-MST across disconnected graphs by calling repeatedly.

    Returns:
        (mst_edges, total_weight) for the component reached from `start`.
    """
    if not adj:
        return [], 0.0
    if start is None:
        start = next(iter(adj))

    local_visited = visited if visited is not None else set()
    mst = []
    total = 0.0

    # if the start node is already visited, nothing to do
    if start in local_visited:
        return [], 0.0

    # min-heap of (weight, from_node, to_node)
    heap = []
    local_visited.add(start)
    for nbr, w in adj.get(start, []):
        heapq.heappush(heap, (w, start, nbr))

    # Continue until we've exhausted reachable nodes from this start
    while heap:
        w, u, v = heapq.heappop(heap)
        if v in local_visited:
            continue
        local_visited.add(v)
        mst.append((u, v, w))
        total += w
        for nbr, nw in adj.get(v, []):
            if nbr not in local_visited:
                heapq.heappush(heap, (nw, v, nbr))

    return mst, total


def prim_full(adj: Dict[Any, List[Tuple[Any, float]]]) -> Tuple[List[Tuple[Any, Any, float]], float]:
    """Run Prim's algorithm across all connected components and return the forest MST.

    This function iterates over all nodes in `adj` and runs `prim_mst` for any
    unvisited node, collecting edges and summing total weight. Useful for
    disconnected graphs where you want a minimum spanning forest.
    """
    all_mst = []
    total = 0.0
    visited = set()
    for node in adj:
        if node in visited:
            continue
        comp_edges, comp_total = prim_mst(adj, start=node, visited=visited)
        all_mst.extend(comp_edges)
        total += comp_total
    return all_mst, total


def build_adj_from_edges(edges: List[Tuple[Any, Any, float]]) -> Dict[Any, List[Tuple[Any, float]]]:
    """Utility: build adjacency dict from undirected edge list."""
    adj: Dict[Any, List[Tuple[Any, float]]] = {}
    for u, v, w in edges:
        adj.setdefault(u, []).append((v, w))
        adj.setdefault(v, []).append((u, w))
    return adj


def _demo():
    # sample undirected graph (nodes can be strings or ints)
    edges = [
        ("A", "B", 4), ("A", "H", 8), ("B", "H", 11),
        ("B", "C", 8), ("H", "I", 7), ("H", "G", 1),
        ("I", "C", 2), ("C", "F", 4), ("C", "D", 7),
        ("G", "F", 2), ("D", "F", 14), ("D", "E", 9),
        ("F", "E", 10), ("G", "I", 6)
    ]

    # include all nodes list (we can derive from edges)
    nodes = sorted({u for u, v, _ in edges} | {v for u, v, _ in edges})

    print("Nodes:", nodes)
    print("Edges:")
    for e in edges:
        print(" ", e)

    # Kruskal
    mst_k, tot_k = kruskal_mst(edges, nodes)
    print("\nKruskal MST edges (u,v,w):")
    for e in mst_k:
        print(" ", e)
    print("Kruskal total weight:", tot_k)

    # Prim
    adj = build_adj_from_edges(edges)
    mst_p, tot_p = prim_mst(adj, start=nodes[0])
    print("\nPrim MST edges (u,v,w):")
    for e in mst_p:
        print(" ", e)
    print("Prim total weight:", tot_p)

    # basic check: total weights should match and MST should have |V|-1 edges
    assert abs(tot_k - tot_p) < 1e-9, "Kruskal and Prim produced different totals"
    assert len(mst_k) == len(nodes) - 1, "Kruskal MST edge count incorrect"
    assert len(mst_p) == len(nodes) - 1, "Prim MST edge count incorrect"

    print("\nDemo assertions passed: MST totals match and edge counts OK.")


if __name__ == '__main__':
    _demo()
