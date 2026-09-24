import time

from .astar import astar
from .bfs import bfs
from .dfs import dfs
from .greedy import greedy
from .puzzle import is_solvable


UNINFORMED = "Uninformed"
INFORMED = "Informed"

SEARCH_TYPES = {
    UNINFORMED: ["BFS", "DFS"],
    INFORMED: ["A*", "GREEDY"]
}

ALGORITHMS = {
    "BFS": bfs,
    "DFS": dfs,
    "A*": astar,
    "GREEDY": greedy
}


def solve(initial_state, algorithm):

    algorithm = algorithm.upper()

    if algorithm not in ALGORITHMS:

        raise ValueError(
            "Algorithm must be one of: "
            + ", ".join(ALGORITHMS)
        )

    if not is_solvable(initial_state):

        raise ValueError(
            "This puzzle configuration has no solution."
        )

    start = time.perf_counter()

    result = ALGORITHMS[algorithm](initial_state)

    end = time.perf_counter()

    result["time"] = end - start
    result["algorithm"] = algorithm

    return result
