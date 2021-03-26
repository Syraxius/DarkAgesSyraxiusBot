import time
import random

from configs.pixel import scan_dist_x, scan_dist_y
from configs.user import run_start_dist

from utils.coords import world_abs_to_rel
from utils.game_actions import walk


def generate_heat_map(coords, heat_distance=3):
    queue = []  # ((x, y), heat_distance)
    heat_map = {}  # (x, y): heat_distance
    for coord in coords:
        queue.append((coord, 0))
    while len(queue) > 0:
        curr = queue.pop(0)

        if curr[0] in heat_map:
            continue

        if curr[1] > heat_distance:
            continue

        heat_map[curr[0]] = curr[1]

        queue.append(((curr[0][0] + 1, curr[0][1]), curr[1] + 1))
        queue.append(((curr[0][0] - 1, curr[0][1]), curr[1] + 1))
        queue.append(((curr[0][0], curr[0][1] + 1), curr[1] + 1))
        queue.append(((curr[0][0], curr[0][1] - 1), curr[1] + 1))

    return heat_map


def get_next_direction_bfs(destination, memory_values, obstacle_set, enemy_set):
    if destination == (0, 0):
        return 0, 0

    next_direction = None

    queue = []  # ((x, y), direction)
    bfs = {}  # (x, y): direction
    queue.append((destination, 'right'))
    while len(queue) > 0:
        curr = queue.pop(0)

        if curr[0] in bfs:
            continue

        if memory_values['pos_x'] + curr[0][0] < 0 or \
            memory_values['pos_x'] + curr[0][0] >= memory_values['size_x'] or \
            memory_values['pos_y'] + curr[0][1] < 0 or \
            memory_values['pos_y'] + curr[0][1] >= memory_values['size_y']:
            continue

        if curr[0] != destination and (curr[0] in obstacle_set or curr[0] in enemy_set):
            continue

        bfs[curr[0]] = curr[1]

        if curr[0] == (0, 0):
            next_direction = curr[1]
            break

        if memory_values['pos_x'] + curr[0][0] - 1 >= 0:
            queue.append(((curr[0][0] - 1, curr[0][1]), 'right'))
        if memory_values['pos_x'] + curr[0][0] + 1 < memory_values['size_x']:
            queue.append(((curr[0][0] + 1, curr[0][1]), 'left'))
        if memory_values['pos_y'] + curr[0][1] - 1 >= 0:
            queue.append(((curr[0][0], curr[0][1] - 1), 'down'))
        if memory_values['pos_y'] + curr[0][1] + 1 < memory_values['size_y']:
            queue.append(((curr[0][0], curr[0][1] + 1), 'up'))

    return next_direction


def get_evade_direction_bfs(memory_values, obstacle_set, enemy_set, min_dist_from_enemy=run_start_dist):
    enemy_heat_map = generate_heat_map(enemy_set, heat_distance=min_dist_from_enemy)

    queue = []  # (x, y)
    bfs = set()  # (x, y)
    queue.append((0, 0))
    while len(queue) > 0:
        curr = queue.pop(0)

        if curr in bfs:
            continue

        if curr in obstacle_set or curr in enemy_set:
            continue

        if curr not in obstacle_set and curr not in enemy_set and curr not in enemy_heat_map:
            return curr

        bfs.add(curr)

        if memory_values['pos_x'] + curr[0] - 1 >= 0:
            queue.append((curr[0] - 1, curr[1]))
        if memory_values['pos_x'] + curr[0] + 1 < memory_values['size_x']:
            queue.append((curr[0] + 1, curr[1]))
        if memory_values['pos_y'] + curr[1] - 1 >= 0:
            queue.append((curr[0], curr[1] - 1))
        if memory_values['pos_y'] + curr[1] + 1 < memory_values['size_y']:
            queue.append((curr[0], curr[1] + 1))

    return None


def move_closer_safely_bfs(hwnd, destination, memory_values, obstacle_set, enemy_set, min_dist_from_enemy=run_start_dist):
    print('Safely going to (rel) %s' % (destination,))
    if destination == (0, 0):
        time.sleep(0.5)
        return

    next_direction = None
    if destination in enemy_set:
        enemy_heat_map = {}
        next_direction = get_next_direction_bfs(destination, memory_values, obstacle_set, enemy_set)
    else:
        for i in range(min_dist_from_enemy, 0 - 1, -1):
            enemy_heat_map = generate_heat_map(enemy_set, heat_distance=i)
            next_direction = get_next_direction_bfs(destination, memory_values, obstacle_set, enemy_heat_map)
            if next_direction is not None:
                break

    if next_direction is None:
        next_direction = random.sample(['up', 'left', 'down', 'right'], 1)[0]

    # Prints the BFS map
    print('-' * 95)
    for y in range(-scan_dist_y, scan_dist_y + 1, 1):
        line = '|'
        for x in range(-scan_dist_x, scan_dist_x + 1, 1):
            if (x, y) == (0, 0):
                line += 'C'
            elif (x, y) in obstacle_set:
                line += 'O'
            elif (x, y) in enemy_set:
                line += 'E'
            elif (x, y) in enemy_heat_map:
                line += '.'
            else:
                line += ' '
            if (x, y) == (0, 0):
                line += {'up': '^', 'right': '>', 'down': 'v', 'left': '<'}[next_direction]
            elif (x, y) == destination:
                line += 'X'
            else:
                line += ' '
            line += ' '
        line += '|'
        print(line)
    print('-' * 95)
    walk(hwnd, next_direction, obstacle_set)


def move_closer_safely_abs_bfs(hwnd, destination, memory_values, obstacle_set, enemy_set):
    move_closer_safely_bfs(hwnd, world_abs_to_rel(memory_values, destination), memory_values, obstacle_set, enemy_set)


def get_nearest_enemy_bfs(obstacle_set, enemy_set, memory_values):
    bfs = set()
    queue = [(0, 0)]
    while len(queue) > 0:
        curr = queue.pop(0)

        if curr in bfs:
            continue

        if curr in obstacle_set:
            continue

        if curr in enemy_set:
            return curr

        bfs.add(curr)

        if memory_values['pos_x'] + curr[0] - 1 >= 0:
            queue.append((curr[0] - 1, curr[1]))
        if memory_values['pos_x'] + curr[0] + 1 < memory_values['size_x']:
            queue.append((curr[0] + 1, curr[1]))
        if memory_values['pos_y'] + curr[1] - 1 >= 0:
            queue.append((curr[0], curr[1] - 1))
        if memory_values['pos_y'] + curr[1] + 1 < memory_values['size_y']:
            queue.append((curr[0], curr[1] + 1))

    return None
