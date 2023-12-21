import random


def calc_neighbors(mine_map, pos):
    neighbors = 0

    for to_check in [(-1, -1), (-1, 0), (-1, 1),
                     (0, -1), (0, 1),
                     (1, -1), (1, 0), (1, 1)]:
        new_pos = (pos[0] + to_check[0], pos[1] + to_check[1])

        if new_pos[0] < 0 or new_pos[0] > len(mine_map) - 1 or new_pos[1] < 0 or new_pos[1] > len(mine_map[0]) - 1:
            continue
        if mine_map[new_pos[0]][new_pos[1]].is_mine():
            neighbors += 1

    return neighbors


def initialize_level(rows, cols):
    return [['#'] * cols for _ in range(rows)]


def randomize_mines(level, mines, start_pos):
    mine_cords = set()

    while True:
        if len(mine_cords) == mines:
            break

        mine_pos = (random.randint(0, len(level) - 1),
                    random.randint(0, len(level[0]) - 1))
        if mine_pos not in mine_cords and mine_pos != start_pos:
            if abs(mine_pos[0] - start_pos[0]) != 1 and abs(mine_pos[1] - start_pos[1]) != 1:
                mine_cords.add(mine_pos)

    return mine_cords


def create_mine_map(blank_map, mine_cords):
    for mine in mine_cords:
        blank_map[mine[0]][mine[1]].set_mine()

    for y in range(len(blank_map)):
        for x in range(len(blank_map[y])):
            if not blank_map[y][x].is_mine():
                blank_map[y][x].set_neighbors(
                    calc_neighbors(blank_map, (y, x)))

    return blank_map


def reveal_empty_squares(start_pos, mine_map):
    visited = [start_pos]
    queue = [start_pos]

    while queue:
        square = queue.pop(0)
        if (mine_map[square[0]][square[1]].get_neighbors() != 0
                or mine_map[square[0]][square[1]].is_mine()):
            continue

        for neighbor in [(-1, -1), (-1, 0), (-1, 1),
                         (0, -1), (0, 1),
                         (1, -1), (1, 0), (1, 1)]:
            new_pos = (square[0] + neighbor[0], square[1] + neighbor[1])

            if not (new_pos[0] < 0 or new_pos[0] > len(mine_map) - 1 or new_pos[1] < 0 or new_pos[1] > len(mine_map[0]) - 1):
                if mine_map[new_pos[0]][new_pos[1]].get_neighbors() == 0:
                    if new_pos not in visited:
                        queue.append(new_pos)
                visited.append(new_pos)
                mine_map[new_pos[0]][new_pos[1]].set_revealed()

    return mine_map


def dig(level, pos, dug_pos_list):
    if level[pos[0]][pos[1]].get_flagged():
        return 0
    if level[pos[0]][pos[1]].is_mine():
        return -1
    if pos in dug_pos_list:
        return -2

    level[pos[0]][pos[1]].set_revealed()
    level = reveal_empty_squares(pos, level)
    return 1
