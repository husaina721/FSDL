import heapq

# Goal state (spiral)
goal_state = [[1, 2, 3],
              [8, 0, 4],
              [7, 6, 5]]

moves = [("Up", -1, 0), ("Down", 1, 0), ("Left", 0, -1), ("Right", 0, 1)]


# ---------- Heuristic (Manhattan Distance) ----------
def manhattan_distance(state):
    distance = 0
    goal_positions = {goal_state[i][j]: (i, j) for i in range(3) for j in range(3)}
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                x, y = goal_positions[value]
                distance += abs(x - i) + abs(y - j)
    return distance


def state_to_tuple(state):
    return tuple(tuple(row) for row in state)


def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j


def print_board(board):
    for row in board:
        print(" ".join(str(x) if x != 0 else "_" for x in row))
    print()


# ---------- Solvability Check ----------
def is_solvable(start, goal):
    def flatten(board):
        return [num for row in board for num in row if num != 0]

    start_flat = flatten(start)
    goal_flat = flatten(goal)

    goal_pos = {val: i for i, val in enumerate(goal_flat)}
    mapped = [goal_pos[val] for val in start_flat]

    inversions = 0
    for i in range(len(mapped)):
        for j in range(i + 1, len(mapped)):
            if mapped[i] > mapped[j]:
                inversions += 1
    return inversions % 2 == 0


# ---------- Reconstruct Path ----------
def reconstruct_path(came_from, move_from, current):
    path, moves_seq = [], []
    while current in came_from:
        path.append(current)
        moves_seq.append(move_from[current])
        current = came_from[current]
    path.append(current)
    return path[::-1], moves_seq[::-1]


# ---------- A* Algorithm ----------
def a_star(start):
    start_tuple = state_to_tuple(start)
    goal_tuple = state_to_tuple(goal_state)

    pq = []
    heapq.heappush(pq, (manhattan_distance(start), 0, start))
    came_from, move_from = {}, {}
    g = {start_tuple: 0}

    while pq:
        _, cost, current = heapq.heappop(pq)
        current_tuple = state_to_tuple(current)

        if current_tuple == goal_tuple:
            return reconstruct_path(came_from, move_from, current_tuple)

        blank_i, blank_j = find_blank(current)

        for direction, dx, dy in moves:
            new_i, new_j = blank_i + dx, blank_j + dy
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [row[:] for row in current]
                new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
                new_tuple = state_to_tuple(new_state)

                tentative_g = g[current_tuple] + 1
                if new_tuple not in g or tentative_g < g[new_tuple]:
                    came_from[new_tuple] = current_tuple
                    move_from[new_tuple] = direction
                    g[new_tuple] = tentative_g
                    f_val = tentative_g + manhattan_distance(new_state)
                    heapq.heappush(pq, (f_val, tentative_g, new_state))

    return None, None


# ---------- Main ----------
if _name_ == "_main_":
    print("Enter the start state (use 0 for blank):")
    start_state = [list(map(int, input(f"Row {i+1}: ").split())) for i in range(3)]

    if not is_solvable(start_state, goal_state):
        print("\nThis puzzle configuration is UNSOLVABLE.")
    else:
        path, moves_seq = a_star(start_state)
        print("\nSteps to solve:\n")
        for i, step in enumerate(path):
            print_board(step)
            if i < len(moves_seq):
                print(f"Move: {moves_seq[i]}")
        print(f"Solved in {len(path)-1} moves.")