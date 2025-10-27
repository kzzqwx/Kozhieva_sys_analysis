import math
from typing import Tuple


def task_from_file(file_path: str, root_id: str) -> Tuple[float, float]:
    with open(file_path, 'r') as file:
        s = file.read()
    return task(s, root_id)


def task(s: str, root_id: str) -> Tuple[float, float]:
    edges = []
    for line in s.strip().split('\n'):
        if line.strip():
            u, v = map(int, line.split(','))
            edges.append((u, v))

    nodes = set()
    for u, v in edges:
        nodes.add(u)
        nodes.add(v)
    n = len(nodes)

    graph = {node: [] for node in nodes}
    for u, v in edges:
        graph[u].append(v)

    r1 = set(edges)

    r2 = set()
    for u, v in edges:
        r2.add((v, u))

    r3 = set()
    for node in nodes:
        for direct_sub in graph.get(node, []):
            for indirect_sub in graph.get(direct_sub, []):
                r3.add((node, indirect_sub))

    r4 = set()
    for u, v in r3:
        r4.add((v, u))

    r5 = set()
    parent_to_children = {}
    for node in nodes:
        parent_to_children[node] = []

    for u, v in edges:
        parent_to_children[u].append(v)

    for parent, children in parent_to_children.items():
        if len(children) > 1:
            for i in range(len(children)):
                for j in range(i + 1, len(children)):
                    r5.add((children[i], children[j]))
                    r5.add((children[j], children[i]))

    relations = [r1, r2, r3, r4, r5]

    l_matrix = {node: [0] * 5 for node in nodes}

    for i, relation in enumerate(relations):
        for node in nodes:
            count = 0
            for u, v in relation:
                if u == node:
                    count += 1
            l_matrix[node][i] = count

    total_entropy = 0.0
    max_possible_connections = n - 1

    for node in nodes:
        node_entropy = 0.0
        for i in range(5):
            lij = l_matrix[node][i]
            if lij > 0:
                p = lij / max_possible_connections
                node_entropy += -p * math.log2(p)
        total_entropy += node_entropy

    c = 1 / (math.e * math.log(2))
    k = 5
    H_ref = c * n * k

    normalized_complexity = total_entropy / H_ref

    return (round(total_entropy, 1), round(normalized_complexity, 1))


if __name__ == "__main__":
    file_path = "task2.csv"
    root = "1"
    result = task_from_file(file_path, root)
    print(f"Энтропия: {result[0]}, Нормированная сложность: {result[1]}")

