
import math
import random


def generate_random_graph(n, density_percent, seed):
    import networkx as nx

    if n < 3:
        raise ValueError("The graph must contain at least 3 vertices.")

    if density_percent not in (12.5, 25, 50, 75):
        raise ValueError("Unsupported graph density.")

    if n > 250000:
        raise ValueError("Too many vertices for the coordinate range.")

    rng = random.Random(seed)
    graph = nx.Graph()

    coordinates = rng.sample(
        [(x, y) for x in range(1, 501) for y in range(1, 501)],
        n
    )

    for node, position in enumerate(coordinates):
        graph.add_node(node, pos=position)

    possible_edges = [
        (u, v)
        for u in range(n)
        for v in range(u + 1, n)
    ]

    edge_count = round(
        len(possible_edges) * density_percent / 100
    )

    selected_edges = rng.sample(possible_edges, edge_count)

    for u, v in selected_edges:
        x1, y1 = coordinates[u]
        x2, y2 = coordinates[v]
        weight = math.hypot(x2 - x1, y2 - y1)
        graph.add_edge(u, v, weight=weight)

    return graph


def calculate_density(graph):
    n = graph.number_of_nodes()

    if n < 2:
        return 0.0

    maximum_edges = n * (n - 1) / 2

    return graph.number_of_edges() / maximum_edges * 100


def calculate_optimality_gap(greedy_cost, optimal_cost):
    if optimal_cost is None or greedy_cost is None:
        return None

    if optimal_cost == 0:
        return 0.0 if greedy_cost == 0 else None

    gap = ((greedy_cost - optimal_cost) / optimal_cost) * 100

    return max(0.0, gap)
