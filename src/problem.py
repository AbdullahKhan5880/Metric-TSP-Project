
import math
import networkx as nx


def validate_graph(graph):
    if not isinstance(graph, nx.Graph):
        raise TypeError("Graph must be a NetworkX graph.")

    if graph.is_directed() or graph.is_multigraph():
        raise ValueError("Graph must be undirected and simple.")

    if graph.number_of_nodes() < 3:
        raise ValueError("Graph must contain at least 3 vertices.")

    for _, _, data in graph.edges(data=True):
        if "weight" not in data:
            raise ValueError("Every edge must have a weight.")

        weight = float(data["weight"])

        if not math.isfinite(weight) or weight <= 0:
            raise ValueError("Edge weights must be positive and finite.")

    return True


def is_valid_tour(graph, tour):
    if tour is None:
        return False

    tour = list(tour)
    nodes = set(graph.nodes())

    if len(tour) != len(nodes):
        return False

    if len(set(tour)) != len(nodes):
        return False

    if set(tour) != nodes:
        return False

    return all(
        graph.has_edge(tour[i], tour[(i + 1) % len(tour)])
        for i in range(len(tour))
    )


def tour_cost(graph, tour):
    if not is_valid_tour(graph, tour):
        raise ValueError("Invalid Hamiltonian cycle.")

    return sum(
        float(graph[tour[i]][tour[(i + 1) % len(tour)]]["weight"])
        for i in range(len(tour))
    )
