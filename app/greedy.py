import heapq
from itertools import count

from .puzzle import (
    MANHATTAN_TABLE,
    NEIGHBOR_TABLE,
    is_goal,
    manhattan_distance,
    rebuild_path,
    swap_state
)


def greedy(initial_state):
    """Greedy best-first search (informed, fast but not optimal).

    Always expands the state that looks closest to the goal according to
    the Manhattan distance, ignoring the cost already spent.
    """

    tie_breaker = count()

    initial_h = manhattan_distance(initial_state)

    open_heap = [(initial_h, next(tie_breaker), initial_state)]

    heuristic = {initial_state: initial_h}

    came_from = {initial_state: None}

    nodes_expanded = 0

    while open_heap:

        _, _, state = heapq.heappop(open_heap)

        nodes_expanded += 1

        if is_goal(state):

            path = rebuild_path(came_from, state)

            return {
                "found": True,
                "path": path,
                "moves": len(path),
                "nodes_expanded": nodes_expanded
            }

        empty = state.index(0)

        h = heuristic[state]

        for move, target in NEIGHBOR_TABLE[empty]:

            neighbor = swap_state(state, empty, target)

            if neighbor in came_from:
                continue

            tile = state[target]

            new_h = (
                h
                + MANHATTAN_TABLE[tile][empty]
                - MANHATTAN_TABLE[tile][target]
            )

            heuristic[neighbor] = new_h
            came_from[neighbor] = (state, move)

            heapq.heappush(
                open_heap,
                (new_h, next(tie_breaker), neighbor)
            )

    return {
        "found": False,
        "path": [],
        "moves": 0,
        "nodes_expanded": nodes_expanded
    }
