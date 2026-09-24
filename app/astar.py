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


def astar(initial_state):
    """A* search (informed, optimal) using the Manhattan distance."""

    tie_breaker = count()

    initial_h = manhattan_distance(initial_state)

    open_heap = [(initial_h, 0, next(tie_breaker), initial_state, 0, initial_h)]

    g_score = {initial_state: 0}

    came_from = {initial_state: None}

    closed = set()

    nodes_expanded = 0

    while open_heap:

        _, _, _, state, g, h = heapq.heappop(open_heap)

        if state in closed:
            continue

        closed.add(state)

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

        new_g = g + 1

        for move, target in NEIGHBOR_TABLE[empty]:

            neighbor = swap_state(state, empty, target)

            if new_g >= g_score.get(neighbor, new_g + 1):
                continue

            tile = state[target]

            new_h = (
                h
                + MANHATTAN_TABLE[tile][empty]
                - MANHATTAN_TABLE[tile][target]
            )

            g_score[neighbor] = new_g
            came_from[neighbor] = (state, move)

            heapq.heappush(
                open_heap,
                (new_g + new_h, -new_g, next(tie_breaker), neighbor, new_g, new_h)
            )

    return {
        "found": False,
        "path": [],
        "moves": 0,
        "nodes_expanded": nodes_expanded
    }
