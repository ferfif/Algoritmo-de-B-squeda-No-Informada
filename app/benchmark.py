import argparse
import os
import statistics
import sys

if __package__:
    from .puzzle import generate_scrambled_state
    from .solver import SEARCH_TYPES, solve
else:
    # Ejecutado como script (python app/benchmark.py): se agrega la raiz
    # del proyecto al path para poder importar "app" como paquete.
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from app.puzzle import generate_scrambled_state
    from app.solver import SEARCH_TYPES, solve


def run_benchmark(algorithm, states):

    nodes_list = []
    time_list = []
    moves_list = []

    for state in states:

        result = solve(state, algorithm)

        nodes_list.append(result["nodes_expanded"])
        time_list.append(result["time"])
        moves_list.append(result["moves"])

    return {
        "algorithm": algorithm,
        "trials": len(states),
        "avg_nodes": statistics.mean(nodes_list),
        "avg_time": statistics.mean(time_list),
        "avg_moves": statistics.mean(moves_list)
    }


def print_report(report):

    print(f"  {report['algorithm']}")
    print(f"    Avg nodes expanded: {report['avg_nodes']:.2f}")
    print(f"    Avg time: {report['avg_time']:.4f}s")
    print(f"    Avg moves: {report['avg_moves']:.2f}")


def main():

    parser = argparse.ArgumentParser(
        description="Benchmark uninformed vs informed search on the 15-puzzle"
    )

    parser.add_argument(
        "--type",
        choices=["uninformed", "informed", "all"],
        default="all",
        help="Which kind of search to run (default: all)"
    )

    parser.add_argument(
        "--trials",
        type=int,
        default=10
    )

    parser.add_argument(
        "--scramble-moves",
        type=int,
        default=20
    )

    args = parser.parse_args()

    # Every algorithm solves the same boards so the comparison is fair.
    states = [
        generate_scrambled_state(args.scramble_moves)
        for _ in range(args.trials)
    ]

    print(
        f"{args.trials} puzzles, "
        f"{args.scramble_moves} scramble moves each\n"
    )

    for search_type, algorithms in SEARCH_TYPES.items():

        if args.type != "all" and args.type != search_type.lower():
            continue

        print(f"{search_type} search")

        for algorithm in algorithms:
            print_report(run_benchmark(algorithm, states))

        print()


if __name__ == "__main__":
    main()
