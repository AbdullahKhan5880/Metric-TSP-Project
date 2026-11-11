
from itertools import permutations
from time import perf_counter

from src.problem import validate_graph


def solve_exhaustive(graph, timeout_seconds=90):
    validate_graph(graph)

    if timeout_seconds is not None and timeout_seconds <= 0:
        raise ValueError("Timeout must be positive or None.")

    start_time = perf_counter()
    nodes = list(graph.nodes())
    start = nodes[0]
    remaining = nodes[1:]
    node_order = {node: index for index, node in enumerate(nodes)}

    best_tour = None
    best_cost = float("inf")
    basic_ops = 0
    tested_configs = 0
    status = "optimal"

    for permutation in permutations(remaining):
        if timeout_seconds is not None:
            if perf_counter() - start_time >= timeout_seconds:
                status = "timeout"
                break

        if node_order[permutation[0]] > node_order[permutation[-1]]:
            continue

        tested_configs += 1
        tour = (start,) + permutation
        total_cost = 0
        valid = True

        for i in range(len(tour)):
            u = tour[i]
            v = tour[(i + 1) % len(tour)]
            basic_ops += 1

            if not graph.has_edge(u, v):
                valid = False
                break

            total_cost += float(graph[u][v]["weight"])

        if valid and total_cost < best_cost:
            best_cost = total_cost
            best_tour = list(tour)

    execution_time = perf_counter() - start_time

    if status != "timeout" and best_tour is None:
        status = "no_tour"

    return {
        "tour": best_tour,
        "cost": best_cost if best_tour is not None else None,
        "basic_ops": basic_ops,
        "tested_configs": tested_configs,
        "execution_time_sec": execution_time,
        "status": status,
    }
