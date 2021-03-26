# world_coords - Actual map coordinates
# map_pixel_coords - Pixel coords on the map
# view_pixel_coords - Pixel coords in the view


def world_coords_to_pixel_coords(world_coords, map_character_center, max_box_pixel_translate):
    right_trans = tuple(world_coords[0] * val for val in max_box_pixel_translate['right'])
    down_trans = tuple(world_coords[1] * val for val in max_box_pixel_translate['down'])
    return map_character_center[0] + right_trans[0] + down_trans[0], map_character_center[1] + right_trans[1] + down_trans[1]


def get_manhattan_distance(relative_world_coords):
    return abs(relative_world_coords[0]) + abs(relative_world_coords[1])


def world_rel_to_abs(memory_values, rel):
    return rel[0] + memory_values['pos_x'], rel[1] + memory_values['pos_y']


def world_abs_to_rel(memory_values, abs):
    return abs[0] - memory_values['pos_x'], abs[1] - memory_values['pos_y']
