from .puzzle import (
    GOAL_STATE,
    NEIGHBOR_TABLE,
    OPPOSITE_MOVE,
    is_goal,
    rebuild_path,
    swap_state
)


def _expand_level(frontier, own, other):
    # Expands a whole BFS level. Returns (meeting_state, next_frontier).
    next_frontier = []

    for state in frontier:

        empty = state.index(0)

        for move, target in NEIGHBOR_TABLE[empty]:

            neighbor = swap_state(state, empty, target)

            if neighbor in own:
                continue

            own[neighbor] = (state, move)

            if neighbor in other:
                return neighbor, next_frontier

            next_frontier.append(neighbor)

    return None, next_frontier


def _join_paths(forward, backward, meeting):
    path = rebuild_path(forward, meeting)

    state = meeting

    while backward[state] is not None:
        state, move = backward[state]
        path.append(OPPOSITE_MOVE[move])

    return path


def bfs(initial_state):
    """Bidirectional breadth-first search (uninformed, optimal).

    Grows one BFS tree from the initial state and another from the goal,
    always expanding the smaller frontier, until both trees touch.
    """

    if is_goal(initial_state):
        return {
            "found": True,
            "path": [],
            "moves": 0,
            "nodes_expanded": 0
        }

    forward = {initial_state: None}
    backward = {GOAL_STATE: None}

    forward_frontier = [initial_state]
    backward_frontier = [GOAL_STATE]

    nodes_expanded = 0

    while forward_frontier and backward_frontier:

        if len(forward_frontier) <= len(backward_frontier):

            nodes_expanded += len(forward_frontier)

            meeting, forward_frontier = _expand_level(
                forward_frontier, forward, backward
            )

        else:

            nodes_expanded += len(backward_frontier)

            meeting, backward_frontier = _expand_level(
                backward_frontier, backward, forward
            )

        if meeting is not None:

            path = _join_paths(forward, backward, meeting)

            return {
                "found": True,
                "path": path,
                "moves": len(path),
                "nodes_expanded": nodes_expanded
            }

    return {
        "found": False,
        "path": [],
        "moves": 0,
        "nodes_expanded": nodes_expanded
    }
