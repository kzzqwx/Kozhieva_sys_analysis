import csv
from collections import deque, defaultdict
import numpy as np

def read_edges_from_csv(path):
    edges = []
    with open(path, newline='', encoding='utf-8') as f:
        r = csv.reader(f)
        for row in r:
            if not row:
                continue
            u = row[0].strip()
            v = row[1].strip() if len(row) > 1 else ''
            if u and v:
                edges.append((u, v))
    return edges

def build_matrices(edges, root):
    if isinstance(edges, str):
        edges_list = read_edges_from_csv(edges)
    else:
        edges_list = list(edges)

    nodes, seen = [], set()
    for u, v in edges_list:
        if u not in seen:
            nodes.append(u); seen.add(u)
        if v not in seen:
            nodes.append(v); seen.add(v)
    if root not in seen:
        raise ValueError("No root")

    idx = {node: i for i, node in enumerate(nodes)}
    n = len(nodes)

    G = defaultdict(list)
    for u, v in edges_list:
        G[u].append(v)
        G[v].append(u)

    A = np.zeros((n, n), dtype=int)
    for u, v in edges_list:
        i, j = idx[u], idx[v]
        A[i, j] = 1
        A[j, i] = 1

    parent = {root: None}
    children = defaultdict(list)
    q = deque([root])
    vis = {root}
    while q:
        u = q.popleft()
        for v in G[u]:
            if v not in vis:
                parent[v] = u
                children[u].append(v)
                vis.add(v)
                q.append(v)

    r1 = np.zeros((n, n), dtype=int)
    for ch, par in parent.items():
        if par is not None:
            r1[idx[par], idx[ch]] = 1
    r2 = r1.T.copy()

    def reach(u):
        s = set()
        q = deque(children.get(u, []))
        while q:
            x = q.popleft()
            if x in s:
                continue
            s.add(x)
            for c in children.get(x, []):
                q.append(c)
        return s

    r3 = np.zeros((n, n), dtype=int)
    for u in nodes:
        for v in reach(u):
            r3[idx[u], idx[v]] = 1
    r3 = (r3 - r1 > 0).astype(int)
    r4 = r3.T.copy()

    r5 = np.zeros((n, n), dtype=int)
    for par, chs in children.items():
        if len(chs) > 1:
            ids = [idx[x] for x in chs]
            for a in ids:
                for b in ids:
                    if a != b:
                        r5[a, b] = 1

    return nodes, A, r1, r2, r3, r4, r5

if __name__ == "__main__":
    edges = [
        ("root", "A"),
        ("root", "B"),
        ("A", "A1"),
        ("A", "A2"),
        ("B", "B1"),
        ("B1", "B1a")
    ]
    root = "root"
    nodes, A, r1, r2, r3, r4, r5 = build_matrices(edges, root)
    print("Узлы:", nodes)
    print("A:\n", A)
    print("r1:\n", r1)
    print("r2:\n", r2)
    print("r3:\n", r3)
    print("r4:\n", r4)
    print("r5:\n", r5)
