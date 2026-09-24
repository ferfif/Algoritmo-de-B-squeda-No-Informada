from .puzzle import GOAL_STATE, NEIGHBOR_TABLE


GOAL_BOARD = list(GOAL_STATE)


def dfs(initial_state):
    """Depth-first search with iterative deepening (uninformed, optimal).

    Runs a depth-limited DFS with a growing limit. It needs no visited set,
    so memory stays proportional to the depth, and it never gets lost in
    an infinite branch. It only avoids undoing the previous move.
    """

    board = list(initial_state)
    path = []
    nodes_visited = 0

    def visit(empty, previous, depth, limit):

        nonlocal nodes_visited

        nodes_visited += 1

        if board == GOAL_BOARD:
            return True

        if depth == limit:
            return False

        for move, target in NEIGHBOR_TABLE[empty]:

            if target == previous:
                continue

            board[empty], board[target] = board[target], board[empty]
            path.append(move)

            if visit(target, empty, depth + 1, limit):
                return True

            path.pop()
            board[empty], board[target] = board[target], board[empty]

        return False

    start = board.index(0)
    limit = 0

    while not visit(start, -1, 0, limit):
        limit += 1

    return {
        "found": True,
        "path": list(path),
        "moves": len(path),
        "nodes_expanded": nodes_visited
    }
