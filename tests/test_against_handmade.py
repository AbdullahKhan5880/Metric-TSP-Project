
from pathlib import Path

import pytest

from src.exhaustive import solve_exhaustive
from src.greedy import solve_greedy
from src.graph_io import load_graph
from src.problem import is_valid_tour, tour_cost, validate_graph


HANDMADE_DIR = (
    Path(__file__).parent.parent
    / "data"
    / "graphs"
    / "handmade"
)

HANDMADE_GRAPHS = {
    "pentagon_5.json": 19.010469622751653,
    "hexagon_6.json": 23.457313802209,
}


@pytest.fixture(params=HANDMADE_GRAPHS.keys())
def handmade_case(request):
    graph = load_graph(HANDMADE_DIR / request.param)
    expected_cost = HANDMADE_GRAPHS[request.param]
    return request.param, graph, expected_cost


def test_graph_validation(handmade_case):
    name, graph, _ = handmade_case

    assert validate_graph(graph)
    assert graph.number_of_nodes() in (5, 6)
    assert graph.number_of_edges() == (
        graph.number_of_nodes() * (graph.number_of_nodes() - 1) // 2
    )


def test_exhaustive_optimal_solution(handmade_case):
    name, graph, expected_cost = handmade_case

    result = solve_exhaustive(graph)

    assert result["status"] == "optimal"
    assert is_valid_tour(graph, result["tour"])
    assert result["cost"] == pytest.approx(expected_cost)


def test_greedy_solution(handmade_case):
    name, graph, expected_cost = handmade_case

    result = solve_greedy(graph)

    assert result["status"] == "feasible"
    assert is_valid_tour(graph, result["tour"])
    assert result["cost"] >= expected_cost - 1e-9


def test_known_tour_cost(handmade_case):
    name, graph, expected_cost = handmade_case

    tour = list(graph.nodes())

    assert tour_cost(graph, tour) == pytest.approx(expected_cost)
