
from time import perf_counter

from src.problem import validate_graph


def solve_greedy(graph):
    validate_graph(graph)

    start_time = perf_counter()
    nodes = list(graph.nodes())
    node_order = {node: index for index, node in enumerate(nodes)}

    best_tour = None
    best_cost = float("inf")
    basic_ops = 0
    tested_configs = 0

    for start in nodes:
        tour = [start]
        unvisited = set(nodes)
        unvisited.remove(start)
        total_cost = 0
        valid = True

        while unvisited:
            current = tour[-1]
            candidates = []

            for node in unvisited:
                basic_ops += 1

                if graph.has_edge(current, node):
                    weight = float(graph[current][node]["weight"])
                    candidates.append((weight, node_order[node], node))

            if not candidates:
                valid = False
                break

            weight, _, next_node = min(candidates)
            tour.append(next_node)
            unvisited.remove(next_node)
            total_cost += weight

        if valid:
            basic_ops += 1

            if graph.has_edge(tour[-1], start):
                total_cost += float(graph[tour[-1]][start]["weight"])
                tested_configs += 1

                if total_cost < best_cost:
                    best_cost = total_cost
                    best_tour = tour

    execution_time = perf_counter() - start_time

    return {
        "tour": best_tour,
        "cost": best_cost if best_tour is not None else None,
        "basic_ops": basic_ops,
        "tested_configs": tested_configs,
        "execution_time_sec": execution_time,
        "status": "feasible" if best_tour is not None else "no_tour",
    }
