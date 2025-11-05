"""A* (A-star) search algorithm implementation with a demo for grid-based games.

This module provides:
- a_star(graph, start, goal, heuristic): generic A* for graphs (adjacency dict)
- build_grid_graph and manhattan heuristic helpers
- a demo that finds a shortest path on a 2D grid with obstacles

Graph representation accepted:
- dict[node] -> list of neighbors, where each neighbor is either:
    - a node (implying cost 1), or
    - a tuple (neighbor, cost)

The implementation returns the shortest path (list of nodes) from start to goal
or an empty list if no path exists.
"""

from typing import Any, Callable, Dict, List, Tuple
import heapq


def _get_neighbors_with_cost(graph: Dict[Any, List[Any]], node: Any) -> List[Tuple[Any, float]]:
    """Normalize neighbor representations to (neighbor, cost) pairs."""
    out: List[Tuple[Any, float]] = []
    for nbr in graph.get(node, []):
        # There are two common styles for adjacency lists:
        # 1) unweighted neighbors as plain nodes (e.g. (x,y) for grid cells)
        # 2) weighted edges as (neighbor, cost)
        # We disambiguate by checking the structure: if `nbr` is a pair whose
        # first element is NOT a primitive (int/float/str/bool), it's likely the
        # weighted form ((neighbor_node), cost). If `nbr` looks like a plain
        # coordinate tuple (int, int) we treat it as an unweighted neighbor.
        if isinstance(nbr, (tuple, list)) and len(nbr) == 2 and isinstance(nbr[1], (int, float)) and not isinstance(nbr[0], (int, float, str, bool)):
            # (neighbor, cost) where neighbor itself may be a tuple/node
            out.append((nbr[0], float(nbr[1])))
        else:
            # neighbor with implicit unit cost
            out.append((nbr, 1.0))
    return out


def reconstruct_path(came_from: Dict[Any, Any], current: Any) -> List[Any]:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def a_star(graph: Dict[Any, List[Any]], start: Any, goal: Any, heuristic: Callable[[Any, Any], float]) -> List[Any]:
    """Run A* search on `graph` from `start` to `goal` using `heuristic`.

    Returns the path as a list of nodes from start to goal, or an empty list if no path.
    """
    open_set = []  # heap of (f_score, count, node)
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))
    came_from: Dict[Any, Any] = {}

    g_score: Dict[Any, float] = {start: 0.0}
    f_score: Dict[Any, float] = {start: heuristic(start, goal)}

    closed = set()
    push_count = 1

    while open_set:
        _, _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        closed.add(current)

        for neighbor, cost in _get_neighbors_with_cost(graph, current):
            if neighbor in closed:
                continue

            tentative_g = g_score.get(current, float('inf')) + cost

            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, goal)
                f_score[neighbor] = f
                heapq.heappush(open_set, (f, push_count, neighbor))
                push_count += 1

    # no path
    return []


def build_grid_graph(width: int, height: int, walls: List[Tuple[int, int]] = None) -> Dict[Tuple[int, int], List[Tuple[int, int]]]:
    """Create a 4-connected grid graph (up/down/left/right). Walls are blocked cells.

    Nodes are (x, y) tuples with 0 <= x < width and 0 <= y < height.
    """
    walls_set = set(walls or [])
    g: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}
    for x in range(width):
        for y in range(height):
            if (x, y) in walls_set:
                continue
            nbrs: List[Tuple[int, int]] = []
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in walls_set:
                    nbrs.append((nx, ny))
            g[(x, y)] = nbrs
    return g


def manhattan(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _demo():
    # Grid demo: find path from top-left to bottom-right with obstacles
    width, height = 8, 6
    walls = [
        (2, 0), (2, 1), (2, 2), (2, 3),
        (4, 2), (5, 2), (6, 2),
    ]
    start = (0, 0)
    goal = (7, 5)

    graph = build_grid_graph(width, height, walls)

    print("Grid size:", width, "x", height)
    print("Start:", start, "Goal:", goal)
    print("Walls:", walls)

    path = a_star(graph, start, goal, lambda n, g: manhattan(n, g))

    if path:
        print("Found path length:", len(path) - 1)
        print(path)
    else:
        print("No path found")

    # Basic checks
    assert path[0] == start, "Path does not start at start"
    assert path[-1] == goal, "Path does not end at goal"
    # Ensure every step is adjacent (Manhattan distance 1)
    for a, b in zip(path, path[1:]):
        assert manhattan(a, b) == 1, f"Non-adjacent steps in path: {a} -> {b}"

    print("\nA* demo assertions passed.")


if __name__ == "__main__":
    _demo()
