#!/usr/bin/python3
import sys
import heapq

class State:
    GOAL_GRID = ["012", "345", "678"]
    def __init__(self):
        self.grid = State.GOAL_GRID[:]
    def to_string(self):
        return "".join(self.grid)
    def to_readable_string(self):
        return "\n".join(self.grid).replace("0", ".")
    def populate_from_string(self, s):
        if sorted(s) != list("012345678"):
            return False
        self.grid[0] = s[0:3]
        self.grid[1] = s[3:6]
        self.grid[2] = s[6:9]
        return True
    def is_goal(self):
        return self.grid == State.GOAL_GRID
    def is_solvable(self):
        s = self.to_string().replace("0", "")
        inversions = 0
        for i in range(0, 8):
            for j in range(i+1, 8):
                if s[i] > s[j]:
                    inversions += 1
        return inversions % 2 == 0

def find_piece(grid, piece):
    for i in range(0, 3):
        for j in range(0, 3):
            if grid[i][j] == str(piece):
                return (i, j)
    return None

def get_neighbors(state):
    position = find_piece(state.grid, 0)
    if position is None:
        raise RuntimeError("invalid state: missing space")
    (pi, pj) = position
    neighbors = []
    displacements = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for displacement in displacements:
        new_pi = pi + displacement[0]
        new_pj = pj + displacement[1]
        if 0 <= new_pi and new_pi < 3 and 0 <= new_pj and new_pj < 3:
            new_grid = list(map(list, state.grid))
            new_grid[pi][pj], new_grid[new_pi][new_pj] = new_grid[new_pi][new_pj], new_grid[pi][pj]
            new_grid = list(map(''.join, new_grid))
            new_state = State()
            new_state.grid = new_grid
            neighbors.append(new_state)
    return neighbors

def l0_distance(grid1, grid2):
    distance = 0
    for value in range(1, 9):
        p1 = find_piece(grid1, value)
        p2 = find_piece(grid2, value)
        if p1 != p2:
            distance += 1
    return distance

def l1_distance(grid1, grid2):
    distance = 0
    for value in range(1, 9):
        p1 = find_piece(grid1, value)
        p2 = find_piece(grid2, value)
        distance += abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    return distance

def compute_heuristic(state):
    #return 0
    #return l0_distance(state.grid, State.GOAL_GRID)
    return l1_distance(state.grid, State.GOAL_GRID)

class Node:
    def __init__(self, parent, state, distance):
        self.parent = parent
        self.state = state
        self.distance = distance
        # in A*, priority (f) = distance (g) + heuristic (h)
        self.priority = self.distance + compute_heuristic(state)
    def __lt__(self, other):
        return self.priority < other.priority
    def __le__(self, other):
        return self.priority <= other.priority
    def __gt__(self, other):
        return self.priority > other.priority
    def __ge__(self, other):
        return self.priority >= other.priority

def retrieve_history(node):
    history = []
    while node is not None:
        history.append(node)
        node = node.parent
    return list(reversed(history))

def solve(initial_state, detailed_output):
    initial_node = Node(None, initial_state, 0)
    final_node = None
    explored_states = 0
    if initial_state.is_goal():
        final_node = initial_node
    elif initial_state.is_solvable():
        explored = set()
        frontier = [initial_node]
        while frontier:
            # Retrieve node from the frontier
            node = heapq.heappop(frontier)
            node_str = node.state.to_string()
            if node_str in explored:
                continue
            # Mark node as explored
            explored |= set([node_str])
            explored_states += 1
            # Perform goal check
            if node.state.is_goal():
                final_node = node
                break
            # Process neighbors
            for new_state in get_neighbors(node.state):
                if new_state.to_string() not in explored:
                    new_node = Node(node, new_state, node.distance+1)
                    heapq.heappush(frontier, new_node)
    if final_node is None:
        print("No solution.")
    else:
        print("Solution in %d step(s)." % final_node.distance)
        if detailed_output:
            print("States explored: %d." % explored_states)
            for node in retrieve_history(final_node):
                print("---")
                print(node.state.to_readable_string())

def main():
    # Read command line arguments
    detailed_output = False;
    if len(sys.argv) == 2 and sys.argv[1] == "detailed":
        detailed_output = True
    # Read input
    line = input()
    initial_state = State()
    if not initial_state.populate_from_string(line):
        sys.stderr.write("Invalid input.\n")
        sys.exit(1)
    # Solve instance
    solve(initial_state, detailed_output)

if __name__ == '__main__':
    main()
