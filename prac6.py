edges = [
    ('A', 'B', 4),
    ('A', 'C', 2),
    ('B', 'C', 1),
    ('B', 'D', 5),
    ('C', 'D', 8),
    ('C', 'E', 10),
    ('D', 'E', 2),
    ('E', 'F', 3)
]

nodes = set()
for u, v, w in edges:
    nodes.add(u)
    nodes.add(v)

parent = {n: n for n in nodes}

def find(n):
    while parent[n] != n:
        n = parent[n]
    return n

def union(a, b):
    pa, pb = find(a), find(b)
    parent[pb] = pa

# Sort edges manually (logical step)
edges.sort(key=lambda x: x[2])

mst = []
total_cost = 0

for u, v, w in edges:
    if find(u) != find(v):
        union(u, v)
        mst.append((u, v, w))
        total_cost += w

print("Edges in MST:")
for u, v, w in mst:
    print(f"{u} -- {v}  cost: {w}")

print("Total cost:", total_cost)