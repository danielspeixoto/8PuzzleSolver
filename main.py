from Config import Config
import pygtrie as trie

########################################################################################################################
# By: Daniel Peixoto / Jonathan Queiroz
# 8-Puzzle Solver using BFS
#
# Ex1.: Solvable instance:
# 1 8 2
# - 4 3
# 7 6 5
# Ex2.: Unsolvable instance:
# 8 1 2
# - 4 3
# 7 6 5
#
# How to write to input
# Ex1.:
# 1
# 8
# 2
# 0
# 4
# 3
# 7
# 6
# 5
########################################################################################################################

initial_config = [[0] * 3 for i in range(3)]
zero_x, zero_y = 0, 0
# Get puzzle config
for i in range(0, 9):
    initial_config[int(i / 3)][int(i % 3)] = int(input())
    if initial_config[int(i / 3)][i % 3] == 0:
        zero_x, zero_y = int(i / 3), i % 3

initial_config = Config(initial_config, zero_x, zero_y, depth=0)

print("Initial Config")
initial_config.print()
print(".")


# Instances are solvable if there is a odd number
# of inversions
def is_solvable(config):
    inversions_count = 0
    for i in range(8):
        if int(config[i]) == 0:
            continue
        for j in range(i + 1, 9):
            if int(config[j]) == 0:
                continue
            if int(config[i]) > int(config[j]):
                inversions_count += 1
    return inversions_count % 2 == 0


if is_solvable(initial_config.code):
    nodes = [initial_config]
    str_config = trie.StringTrie()
    str_config[initial_config.code] = True

    i = 0
    attempts = 0
    print("Looking for a solution...")
    while not nodes[i].correct():
        for var in nodes[i].variations():
            attempts += 1
            # Makes a copy of the old configuration
            new_config = [row[:] for row in nodes[i].config]

            # Switch positions
            new_config[nodes[i].zero_x][nodes[i].zero_y],\
            new_config[nodes[i].zero_x + var[0]][nodes[i].zero_y + var[1]] = \
                new_config[nodes[i].zero_x + var[0]][nodes[i].zero_y + var[1]],\
                new_config[nodes[i].zero_x][nodes[i].zero_y]

            # Add to queue
            new_config = Config(new_config, nodes[i].zero_x + var[0], nodes[i].zero_y + var[1], nodes[i], nodes[i].depth + 1)
            # Checks if new config is already discovered
            if not str_config.has_key(new_config.code):
                nodes.append(new_config)
                str_config[new_config.code] = True
                # Uncomment if you want to know how many nodes are found and how many attempts were made
                # print("Nodes/Attempts = " + str(len(nodes)) + "/" + str(attempts))
        i += 1

    depth = nodes[i].depth
    print("Answer: " + str(depth))

    def recreate_movements(node : Config):
        if node.parent is not None:
            recreate_movements(node.parent)
            print("Movement " + str(node.depth))
            node.print()

    # Moves to solution
    recreate_movements(nodes[i])
else:
    print("Instance is not solvable")