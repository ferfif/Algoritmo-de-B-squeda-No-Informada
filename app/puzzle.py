import random


GOAL_STATE = (
    1, 2, 3, 4,
    5, 6, 7, 8,
    9, 10, 11, 12,
    13, 14, 15, 0
)


OPPOSITE_MOVE = {
    "UP": "DOWN",
    "DOWN": "UP",
    "LEFT": "RIGHT",
    "RIGHT": "LEFT"
}


def _build_neighbor_table():
    table = []

    for index in range(16):
        row, col = index // 4, index % 4
        options = []

        if row > 0:
            options.append(("UP", index - 4))
        if row < 3:
            options.append(("DOWN", index + 4))
        if col > 0:
            options.append(("LEFT", index - 1))
        if col < 3:
            options.append(("RIGHT", index + 1))

        table.append(tuple(options))

    return tuple(table)


def _build_manhattan_table():
    table = [[0] * 16]

    for value in range(1, 16):
        goal_row, goal_col = (value - 1) // 4, (value - 1) % 4
        table.append([
            abs(index // 4 - goal_row) + abs(index % 4 - goal_col)
            for index in range(16)
        ])

    return table


# NEIGHBOR_TABLE[empty_index] -> ((move, target_index), ...)
NEIGHBOR_TABLE = _build_neighbor_table()

# MANHATTAN_TABLE[value][index] -> distance of that tile to its goal cell
MANHATTAN_TABLE = _build_manhattan_table()


def swap_state(state, empty, target):
    new_state = list(state)
    new_state[empty], new_state[target] = new_state[target], new_state[empty]
    return tuple(new_state)


def is_solvable(state):
    tiles = [value for value in state if value != 0]

    inversions = sum(
        1
        for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
        if tiles[i] > tiles[j]
    )

    blank_row_from_bottom = 4 - state.index(0) // 4

    return (inversions + blank_row_from_bottom) % 2 == 1


def rebuild_path(came_from, state):
    path = []

    while came_from[state] is not None:
        state, move = came_from[state]
        path.append(move)

    path.reverse()

    return path


def find_empty_position(state):
    return state.index(0)


def get_position(index):
    return index // 4, index % 4


def get_valid_moves(state):
    empty = find_empty_position(state)
    row, col = get_position(empty)

    moves = []

    if row > 0:
        moves.append("UP")

    if row < 3:
        moves.append("DOWN")

    if col > 0:
        moves.append("LEFT")

    if col < 3:
        moves.append("RIGHT")

    return moves


def apply_move(state, move):
    empty = find_empty_position(state)

    if move == "UP":
        target = empty - 4
    elif move == "DOWN":
        target = empty + 4
    elif move == "LEFT":
        target = empty - 1
    elif move == "RIGHT":
        target = empty + 1
    else:
        raise ValueError("Invalid move")

    new_state = list(state)

    new_state[empty], new_state[target] = (
        new_state[target],
        new_state[empty]
    )

    return tuple(new_state)


def get_neighbors(state):
    empty = state.index(0)

    return [
        (move, swap_state(state, empty, target))
        for move, target in NEIGHBOR_TABLE[empty]
    ]


def is_goal(state):
    return state == GOAL_STATE


def manhattan_distance(state):
    total = 0

    for index, value in enumerate(state):

        if value == 0:
            continue

        goal_row, goal_col = get_position(value - 1)
        row, col = get_position(index)

        total += abs(row - goal_row) + abs(col - goal_col)

    return total


def generate_scrambled_state(moves=10):
    state = GOAL_STATE
    previous_move = None

    for _ in range(moves):

        valid_moves = get_valid_moves(state)

        if previous_move:
            opposite = {
                "UP": "DOWN",
                "DOWN": "UP",
                "LEFT": "RIGHT",
                "RIGHT": "LEFT"
            }

            if opposite[previous_move] in valid_moves:
                valid_moves.remove(opposite[previous_move])

        move = random.choice(valid_moves)

        state = apply_move(state, move)

        previous_move = move

    return state