import time
import random

from configs.user import assail_mode, spell_list, mp_low, mp_high, hp_low, hp_high, run_start_dist, run_stop_dist, rest_avoid_dist
from configs.map import map_waypoints
from configs.pixel import view_character_center, view_box_pixel_translate

from utils.handle import get_winlist, get_hwnd
from utils.pixel import get_image_background, get_relative_map_and_enemy_set
from utils.memory import get_static_object_tile_pass, get_all_memory_values
from utils.coords import get_manhattan_distance
from utils.game_actions import walk, refresh, assail_enemy, use_spell_on_enemy
from utils.pathfinding import get_nearest_enemy_bfs, move_closer_safely_abs_bfs, move_closer_safely_bfs, get_evade_direction_bfs


def main():
    winlist = get_winlist()
    hwnd = get_hwnd('darkages', winlist)
    sotp = get_static_object_tile_pass()

    refresh_counter = 100
    rest = False
    run = False
    out_of_range_nearest_enemy = None
    random_steps_left = 0
    random_direction = random.sample(['up', 'down', 'left', 'right'], 1)[0]

    while True:
        if refresh_counter % 100 == 0:
            time.sleep(1)
            refresh(hwnd)
        refresh_counter += 1

        print('-' * 5)

        # Use pixel scan to get enemy location
        img = get_image_background(hwnd, 1280, 960, 3, 26)
        _, enemy_set, _ = get_relative_map_and_enemy_set(img)
        print('Found %s enemies at %s' % (len(enemy_set), enemy_set))

        # Use memory reading to get everything else
        memory_values = get_all_memory_values(hwnd, sotp)
        obstacle_set = memory_values['obstacle_set_rel']
        waypoints = map_waypoints.get(memory_values['map'], {})
        if waypoints and 'virtual_obstacles' in waypoints:
            for virtual_obstacle in waypoints['virtual_obstacles']:
                virtual_obstacle_rel = (virtual_obstacle[0] - memory_values['pos_x'], virtual_obstacle[1] - memory_values['pos_y'])
                obstacle_set.add(virtual_obstacle_rel)
        if waypoints and 'ignored_obstacles' in waypoints:
            for ignored_obstacle in waypoints['ignored_obstacles']:
                ignored_obstacle_rel = (ignored_obstacle[0] - memory_values['pos_x'], ignored_obstacle[1] - memory_values['pos_y'])
                if ignored_obstacle_rel in obstacle_set:
                    obstacle_set.remove(ignored_obstacle_rel)
        print('Current values: %s' % (memory_values,))

        # Find the nearest enemy
        nearest_enemy = get_nearest_enemy_bfs(obstacle_set, enemy_set, memory_values)
        print('Nearest enemy is %s' % (nearest_enemy,))

        # Decide whether to rest or not
        if memory_values['mp'] < mp_low or memory_values['hp'] < hp_low:
            rest = True
        if waypoints and waypoints.get('is_home', False) and (memory_values['mp'] < mp_high or memory_values['hp'] < hp_high):
            rest = True
        if memory_values['mp'] > mp_high and memory_values['hp'] > hp_high:
            rest = False

        _run_start_dist = run_start_dist
        _run_stop_dist = run_stop_dist

        # Decide whether to run or not
        if nearest_enemy:
            if rest:
                _run_start_dist = rest_avoid_dist
                _run_stop_dist = rest_avoid_dist
            if get_manhattan_distance(nearest_enemy) < _run_start_dist:
                run = True
            if get_manhattan_distance(nearest_enemy) > _run_stop_dist:
                run = False
        else:
            run = False

        # Decide whether to rest, run or go to training grounds
        if rest:
            rest_coords = waypoints.get('rest')
            if rest_coords:
                print('Resting or going to rest point!')
                if waypoints.get('is_home', False) or nearest_enemy:
                    move_closer_safely_bfs(hwnd, rest_coords, memory_values, obstacle_set, enemy_set)
                else:
                    print('No enemies, resting here!')
                    time.sleep(1)
                continue
        elif run:
            nearest_safe_tile = get_evade_direction_bfs(memory_values, obstacle_set, enemy_set, min_dist_from_enemy=_run_stop_dist)
            if nearest_safe_tile is None:
                nearest_safe_tile = random.sample(['up', 'down', 'left', 'right'], 1)[0]
                if 'rest' in waypoints:
                    nearest_safe_tile = waypoints['rest']
            print('Running to nearest safe tile at %s' % (nearest_safe_tile,))
            move_closer_safely_bfs(hwnd, nearest_safe_tile, memory_values, obstacle_set, enemy_set)
            continue
        else:
            training_grounds_coords = waypoints.get('training_grounds_coords')
            if training_grounds_coords:
                print('Walking to training grounds!')
                move_closer_safely_abs_bfs(hwnd, training_grounds_coords, memory_values, obstacle_set, enemy_set)
                continue

        # Already at training grounds, and not resting or running

        # Attack nearest enemy
        if nearest_enemy:
            if assail_mode:
                attacked = assail_enemy(hwnd, nearest_enemy)
            else:
                attacked = use_spell_on_enemy(hwnd, spell_list, nearest_enemy, view_character_center, view_box_pixel_translate)
            if not attacked:
                out_of_range_nearest_enemy = (nearest_enemy[0] + memory_values['pos_x'], nearest_enemy[1] + memory_values['pos_y'])
            else:
                out_of_range_nearest_enemy = None
                continue

        # Move to last known nearest enemy
        if out_of_range_nearest_enemy:
            print('Trying to get nearer to enemy at %s' % (out_of_range_nearest_enemy,))
            if get_manhattan_distance((out_of_range_nearest_enemy[0] - memory_values['pos_x'], out_of_range_nearest_enemy[1] - memory_values['pos_y'])) > run_start_dist:
                move_closer_safely_abs_bfs(hwnd, out_of_range_nearest_enemy, memory_values, obstacle_set, enemy_set)
                continue
            else:
                out_of_range_nearest_enemy = None

        print('Searching for enemies...')

        # Patrol if patrol list is available
        patrol_coords_list = waypoints.get('patrol')
        if patrol_coords_list:
            curr_patrol_coords, min_dist = waypoints.get('curr_patrol_coords', (None, 0))
            if curr_patrol_coords is None:
                curr_patrol_coords, min_dist = patrol_coords_list[0]
            print('Patrolling to %s' % (curr_patrol_coords, ))
            move_closer_safely_abs_bfs(hwnd, curr_patrol_coords, memory_values, obstacle_set, enemy_set)
            dist_to_patrol_coords = abs(curr_patrol_coords[0] - memory_values['pos_x']) + abs(curr_patrol_coords[1] - memory_values['pos_y'])
            if dist_to_patrol_coords - 1 <= min_dist:
                try:
                    curr_patrol_coords, min_dist = patrol_coords_list[(patrol_coords_list.index((curr_patrol_coords, min_dist)) + 1) % len(patrol_coords_list)]
                except ValueError:
                    curr_patrol_coords, min_dist = patrol_coords_list[0]
                time.sleep(1)  # Wait longer for map load
            waypoints['curr_patrol_coords'] = (curr_patrol_coords, min_dist)
            continue

        # Walk randomly if patrol list is not available
        if random_steps_left <= 0:
            random_direction = random.sample(['up', 'down', 'left', 'right'], 1)[0]
            random_steps_left = random.randint(0, 20)
        random_steps_left -= 1
        walk(hwnd, random_direction, obstacle_set)


if __name__ == '__main__':
    main()
