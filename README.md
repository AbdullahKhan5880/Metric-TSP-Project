# P39 - Metric Traveling Salesperson Problem

**Course:** Advanced Algorithms  
**Academic Year:** 2026/2027  
**Project Phase:** Project 1 - Exhaustive Search and Greedy Heuristics  
**Student Name:** Muhammad Abdullah Khan Akazai  
**Student ID:** 138367  
**Program:** Master in Computational Engineering

## 1. Project Overview

This project studies the Traveling Salesperson Problem (TSP), specifically P39 - Metric Traveling Salesperson Problem.

Given an undirected weighted graph, the objective is to find a minimum-cost Hamiltonian cycle that visits every vertex exactly once and returns to the starting vertex.

If no Hamiltonian cycle exists, the algorithm reports that no tour was found.

The project implements and compares two approaches:

- **Exhaustive Search:** Searches the possible Hamiltonian cycles to find an optimal solution.
- **Greedy Heuristic:** Uses a multi-start nearest-neighbour strategy to find feasible solutions efficiently.

## 2. Technologies

- Python
- NetworkX
- NumPy
- Matplotlib
- Pandas
- Pytest

## 3. Project Structure

```text
Metric-TSP-Project/
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ problem.py
â”‚   â”œâ”€â”€ exhaustive.py
â”‚   â”œâ”€â”€ greedy.py
â”‚   â”œâ”€â”€ graph_io.py
â”‚   â””â”€â”€ utils.py
â”œâ”€â”€ experiments/
â”‚   â””â”€â”€ run_p1_benchmarks.py
â”œâ”€â”€ data/
â”‚   â”œâ”€â”€ graphs/
â”‚   â”‚   â”œâ”€â”€ handmade/
â”‚   â”‚   â””â”€â”€ synthetic/
â”‚   â””â”€â”€ results.csv
â”œâ”€â”€ notebooks/
â”œâ”€â”€ docs/
â”‚   â””â”€â”€ p1/
â”œâ”€â”€ tests/
â”‚   â””â”€â”€ test_against_handmade.py
â”œâ”€â”€ requirements.txt
â””â”€â”€ README.md
```

## 4. Installation

Create and activate a Python virtual environment:

```bash
python -m venv .venv
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## 5. Algorithms

### 5.1 Exhaustive Search

The exhaustive solver enumerates possible vertex orderings while fixing the starting vertex and avoiding duplicate reverse-direction cycles.

For every candidate cycle, it checks whether all required edges exist and calculates its total weight.

The solver supports a configurable timeout. It can return:

- `optimal`: An optimal Hamiltonian cycle was found and the search completed.
- `no_tour`: The search completed without finding a Hamiltonian cycle.
- `timeout`: The search exceeded its time limit.

The worst-case time complexity is factorial:

\[
O((N-1)!)
\]

### 5.2 Greedy Heuristic

The greedy solver uses a multi-start nearest-neighbour strategy.

It tries each vertex as a starting point, repeatedly selects the nearest unvisited adjacent vertex, and finally checks whether it can return to the starting vertex.

It returns:

- `feasible`: A Hamiltonian cycle was found.
- `no_tour`: The heuristic did not find a Hamiltonian cycle.

A `no_tour` result from the greedy algorithm does not prove that the graph has no Hamiltonian cycle.

The straightforward implementation has a worst-case time complexity of:

\[
O(N^3)
\]

## 6. Graph Generation

Synthetic graphs are generated using randomly selected, non-coincident two-dimensional integer coordinates.

Coordinate values are within the range [1, 500].

Edge weights are calculated using Euclidean distance.

The target graph densities are:

- 12.5%
- 25%
- 50%
- 75%

The random seed is based on the student ID: `138367`.

Graphs are saved in JSON format under:

`data/graphs/synthetic/`

Because edges are selected randomly, some generated graphs may not contain a Hamiltonian cycle.

## 7. Testing

Run the automated tests using:

```bash
python -m pytest -v
```

Hand-crafted graphs are stored in:

`data/graphs/handmade/`

The tests check graph validation, exhaustive optimal solutions, greedy solutions, and known tour costs.

## 8. Running Experiments

Run the benchmark experiment using:

```bash
python experiments/run_p1_benchmarks.py
```

The experiment evaluates both algorithms for different graph sizes and densities.

A timeout of 90 seconds is used for each exhaustive-search run.

The results are stored in:

`data/results.csv`

## 9. Performance Measurements

The benchmark records:

- `basic_ops`: Number of operations counted by the implementation.
- `execution_time_sec`: Execution time in seconds.
- `tested_configs`: Number of configurations counted by the solver.
- `solution_quality`: Cost of the returned tour, when available.
- `optimality_gap_pct`: Percentage difference between the greedy solution and the optimal solution, when an optimal result is available.
- `status`: Solver outcome.

The optimality gap is calculated as:

\[
\text{Gap} =
\frac{\text{Greedy Cost} - \text{Optimal Cost}}
{\text{Optimal Cost}} \times 100
\]

The gap is only calculated when an optimal solution and a greedy tour are both available.

## 10. Current Experimental Observations

In the current benchmark run:

- All four tested configurations with \(N=12\) completed exhaustive search within the 90-second timeout.
- All four tested configurations with \(N=14\) reached the timeout.
- The greedy heuristic completed much faster but did not always find a feasible tour.

These observations apply to the tested instances and execution environment; they do not establish a universal maximum graph size.

## 11. Metric TSP and Graph Density Note

The edge weights are Euclidean distances between the generated 2D points. Euclidean distance satisfies the triangle inequality.

However, the synthetic generator selects only a percentage of possible edges. Therefore, these graphs are generally sparse subgraphs rather than complete metric graphs. The algorithms operate on the generated weighted graphs, and a Hamiltonian cycle may not exist.

This distinction is important when interpreting the results in the context of the Metric TSP problem.

## 12. Limitations

- Exhaustive Search becomes computationally expensive as the number of vertices increases.
- The Greedy Heuristic does not guarantee an optimal solution.
- The Greedy Heuristic may fail to find a tour even when one exists.
- Randomly generated sparse graphs may not contain a Hamiltonian cycle.
- Benchmark results depend on the generated instances and execution environment.

## 13. Project Status

Project 1 implementation and initial benchmark experiments have been completed. Further analysis, visualizations, documentation, and final validation are part of the remaining project work.
