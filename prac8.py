"""Kruskal's Minimal Spanning Tree Algorithm Implementation (Greedy Approach).

This implementation demonstrates Kruskal's algorithm, which builds an MST by:
1. Sorting all edges by weight (the greedy choice)
2. Adding edges in ascending weight order if they don't create cycles
3. Using Union-Find data structure for efficient cycle detection

Key components:
- UnionFind class: Implements disjoint sets with path compression and rank
- kruskal_mst: Main algorithm implementation
- Visualization of the greedy choice at each step
"""

from typing import List, Tuple, Set, Dict, Any
from dataclasses import dataclass
import time


class UnionFind:
    """Disjoint Set data structure with path compression and union by rank."""
    
    def __init__(self, nodes: List[Any]):
        self.parent = {x: x for x in nodes}
        self.rank = {x: 0 for x in nodes}
    
    def find(self, x: Any) -> Any:
        """Find set representative with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]
    
    def union(self, x: Any, y: Any) -> bool:
        """Union by rank. Returns True if sets were different."""
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        
        # Union by rank
        if self.rank[px] < self.rank[py]:
            self.parent[px] = py
        elif self.rank[px] > self.rank[py]:
            self.parent[py] = px
        else:
            self.parent[py] = px
            self.rank[px] += 1
        return True


@dataclass
class Edge:
    """Edge in a weighted graph."""
    src: Any
    dst: Any
    weight: float

    def __str__(self) -> str:
        return f"{self.src} --({self.weight})--> {self.dst}"


def kruskal_mst(edges: List[Edge], nodes: List[Any], verbose: bool = True) -> Tuple[List[Edge], float]:
    """Kruskal's MST algorithm implementation.
    
    Args:
        edges: List of Edge objects representing the graph's edges
        nodes: List of all nodes in the graph
        verbose: If True, prints progress of the algorithm
    
    Returns:
        Tuple of (MST edges list, total weight)
    """
    # Sort edges by weight (the greedy choice)
    sorted_edges = sorted(edges, key=lambda e: e.weight)
    if verbose:
        print("\nSorted edges by weight:")
        for e in sorted_edges:
            print(f"  {e}")
    
    uf = UnionFind(nodes)
    mst: List[Edge] = []
    total_weight = 0.0
    
    if verbose:
        print("\nBuilding MST:")
        print("  (Each step shows the greedy choice made)\n")
    
    for edge in sorted_edges:
        if len(mst) == len(nodes) - 1:
            break  # MST complete
        
        if uf.union(edge.src, edge.dst):
            mst.append(edge)
            total_weight += edge.weight
            if verbose:
                print(f"  Added: {edge}")
                print(f"  Current MST weight: {total_weight}")
                time.sleep(0.5)  # Pause to show progress
    
    return mst, total_weight


def create_sample_graph() -> Tuple[List[Edge], List[Any]]:
    """Creates a sample weighted undirected graph."""
    # Create edges (each edge added once, treated as undirected)
    edges = [
        Edge('A', 'B', 4), Edge('A', 'H', 8),
        Edge('B', 'C', 8), Edge('B', 'H', 11),
        Edge('C', 'D', 7), Edge('C', 'F', 4),
        Edge('C', 'I', 2), Edge('D', 'E', 9),
        Edge('D', 'F', 14), Edge('E', 'F', 10),
        Edge('F', 'G', 2), Edge('G', 'H', 1),
        Edge('G', 'I', 6), Edge('H', 'I', 7),
    ]
    
    # Extract unique nodes
    nodes = sorted(set(
        [e.src for e in edges] +
        [e.dst for e in edges]
    ))
    
    return edges, nodes


def _demo():
    """Demonstrates Kruskal's algorithm with a sample graph."""
    print("Kruskal's MST Algorithm Demo")
    print("=" * 40)
    
    # Create and show sample graph
    edges, nodes = create_sample_graph()
    
    print("Graph:")
    print("  Vertices:", nodes)
    print("\n  Edges:")
    for e in edges:
        print(f"    {e}")
    
    # Run Kruskal's algorithm
    mst, total = kruskal_mst(edges, nodes, verbose=True)
    
    print("\nFinal Results:")
    print("-" * 20)
    print("MST edges:")
    for edge in mst:
        print(f"  {edge}")
    print(f"\nTotal MST weight: {total}")
    
    # Verify MST properties
    assert len(mst) == len(nodes) - 1, "MST should have |V|-1 edges"
    
    # Verify connectivity (all nodes appear in MST)
    mst_nodes = set()
    for edge in mst:
        mst_nodes.add(edge.src)
        mst_nodes.add(edge.dst)
    assert mst_nodes == set(nodes), "MST should include all nodes"
    
    print("\nAll assertions passed: MST properties verified!")


if __name__ == '__main__':
    _demo()
