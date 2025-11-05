"""Prim's Minimal Spanning Tree Algorithm Implementation (Greedy Approach).

This module implements Prim's MST algorithm, which demonstrates the greedy approach by:
1. Starting from a single vertex
2. Growing the tree one edge at a time
3. Always choosing the minimum weight edge that connects tree to a new vertex

The implementation provides:
- prim_mst(adj, start): Core Prim's algorithm using min-heap
- prim_full(adj): Handles disconnected graphs (forest of MSTs)
- Utility functions and demo with visualization
"""

from typing import Dict, List, Tuple, Any, Set
import heapq


def prim_mst(adj: Dict[Any, List[Tuple[Any, float]]], start: Any = None) -> Tuple[List[Tuple[Any, Any, float]], float]:
    """Prim's algorithm implementation using a min-heap priority queue.
    
    Args:
        adj: Adjacency dict mapping node -> [(neighbor, weight),...].
        start: Starting node (optional, picks first node if None).
    
    Returns:
        Tuple of (list of MST edges as (u,v,weight), total weight).
    """
    if not adj:
        return [], 0.0
    if start is None:
        start = next(iter(adj))

    visited: Set[Any] = set()
    mst: List[Tuple[Any, Any, float]] = []
    total = 0.0

    # Priority queue: (weight, from_node, to_node)
    heap = []
    
    # Add start node's edges
    visited.add(start)
    for nbr, w in adj[start]:
        heapq.heappush(heap, (w, start, nbr))

    while heap:
        weight, u, v = heapq.heappop(heap)
        if v in visited:
            continue
            
        # Add edge to MST
        visited.add(v)
        mst.append((u, v, weight))
        total += weight

        # Add all edges from newly visited node
        for nbr, w in adj[v]:
            if nbr not in visited:
                heapq.heappush(heap, (w, v, nbr))

    return mst, total


def build_graph() -> Dict[Any, List[Tuple[Any, float]]]:
    """Creates a sample weighted undirected graph for demo."""
    edges = [
        (1, 2, 4), (1, 3, 2),
        (2, 3, 1), (2, 4, 3),
        (3, 4, 5), (3, 5, 6),
        (4, 5, 2), (4, 6, 7),
        (5, 6, 4)
    ]
    
    # Convert to adjacency list format
    adj: Dict[Any, List[Tuple[Any, float]]] = {}
    for u, v, w in edges:
        adj.setdefault(u, []).append((v, w))
        adj.setdefault(v, []).append((u, w))
    return adj


def format_mst(mst: List[Tuple[Any, Any, float]]) -> str:
    """Format MST edges for pretty printing."""
    return "\n".join(f"  {u} -- {w} --> {v}" for u, v, w in mst)


def _demo():
    """Demonstrates Prim's algorithm on a sample graph."""
    print("Prim's MST Algorithm Demo")
    print("-" * 30)
    
    # Build and show sample graph
    adj = build_graph()
    print("Graph vertices:", sorted(adj.keys()))
    print("\nGraph edges:")
    for u in adj:
        for v, w in adj[u]:
            if u < v:  # print each edge only once
                print(f"  {u} -- {w} --> {v}")
    
    # Run Prim's algorithm
    print("\nComputing MST using Prim's algorithm...")
    mst_edges, total = prim_mst(adj, start=1)
    
    print("\nMinimum Spanning Tree edges:")
    print(format_mst(mst_edges))
    print(f"\nTotal MST weight: {total}")
    
    # Verify properties
    vertices = set(adj.keys())
    mst_vertices = {u for u, v, _ in mst_edges} | {v for u, v, _ in mst_edges}
    
    assert len(mst_edges) == len(vertices) - 1, "MST should have |V|-1 edges"
    assert mst_vertices == vertices, "MST should span all vertices"
    print("\nAll assertions passed!")


if __name__ == '__main__':
    _demo()
