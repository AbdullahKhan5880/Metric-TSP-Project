
import csv
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.exhaustive import solve_exhaustive
from src.greedy import solve_greedy
from src.graph_io import save_graph
from src.utils import (
    calculate_density,
    calculate_optimality_gap,
    generate_random_graph,
)


SYNTHETIC_DIR = PROJECT_ROOT / "data" / "graphs" / "synthetic"
RESULTS_FILE = PROJECT_ROOT / "data" / "results.csv"

STUDENT_ID = 138367
PROBLEM_ID = "P39"
PROJECT_PHASE = "P1"
TIMEOUT_SECONDS = 90

DENSITIES = (12.5, 25, 50, 75)
VERTEX_COUNTS = (4, 6, 8, 10, 12, 14, 16)


def run_benchmarks():
    SYNTHETIC_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    columns = [
        "student_id",
        "problem_id",
        "project_phase",
        "N",
        "density",
        "seed",
        "solver_type",
        "basic_ops",
        "execution_time_sec",
        "tested_configs",
        "solution_quality",
        "optimality_gap_pct",
        "status",
    ]

    rows = []

    for n in VERTEX_COUNTS:
        for density in DENSITIES:
            graph = generate_random_graph(
                n=n,
                density_percent=density,
                seed=STUDENT_ID,
            )

            actual_density = calculate_density(graph)

            graph_name = (
                f"n{n}_density{density}_seed{STUDENT_ID}.json"
            )
            save_graph(graph, SYNTHETIC_DIR / graph_name)

            exact_result = solve_exhaustive(
                graph,
                timeout_seconds=TIMEOUT_SECONDS,
            )

            greedy_result = solve_greedy(graph)

            gap = None

            if exact_result["status"] == "optimal":
                gap = calculate_optimality_gap(
                    greedy_result["cost"],
                    exact_result["cost"],
                )

            for solver_name, result in (
                ("exhaustive", exact_result),
                ("greedy", greedy_result),
            ):
                if solver_name == "greedy":
                    optimality_gap = gap
                elif exact_result["status"] == "optimal":
                    optimality_gap = 0.0
                else:
                    optimality_gap = None

                rows.append({
                    "student_id": STUDENT_ID,
                    "problem_id": PROBLEM_ID,
                    "project_phase": PROJECT_PHASE,
                    "N": n,
                    "density": density,
                    "seed": STUDENT_ID,
                    "solver_type": solver_name,
                    "basic_ops": result["basic_ops"],
                    "execution_time_sec": result["execution_time_sec"],
                    "tested_configs": result["tested_configs"],
                    "solution_quality": result["cost"],
                    "optimality_gap_pct": optimality_gap,
                    "status": result["status"],
                })

            print(
                f"N={n}, target density={density}%, "
                f"actual density={actual_density:.2f}%: "
                f"exact={exact_result['status']}, "
                f"greedy={greedy_result['status']}"
            )

    with RESULTS_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nResults saved to: {RESULTS_FILE}")


if __name__ == "__main__":
    run_benchmarks()
