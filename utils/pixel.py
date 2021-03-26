from PIL import Image

import win32con
import win32gui
import win32ui

from configs.pixel import scan_dist_x, scan_dist_y, character_color, enemy_color, obstacle_color, map_character_center, max_box_pixel_translate

from utils.coords import world_coords_to_pixel_coords


def get_image_background(hwnd, width, height, off_x, off_y):
    # Get bitmap data
    window_dc = win32gui.GetWindowDC(hwnd)
    dc = win32ui.CreateDCFromHandle(window_dc)
    compatible_dc = dc.CreateCompatibleDC()
    data_bit_map = win32ui.CreateBitmap()
    data_bit_map.CreateCompatibleBitmap(dc, width, height)
    compatible_dc.SelectObject(data_bit_map)
    compatible_dc.BitBlt((0, 0), (width, height), dc, (off_x, off_y), win32con.SRCCOPY)

    # Save to file
    data_bit_map.SaveBitmapFile(compatible_dc, 'screenshot.bmp')

    # Convert to PIL image
    bmp_info = data_bit_map.GetInfo()
    bmp_str = data_bit_map.GetBitmapBits(True)
    im = Image.frombuffer('RGB', (bmp_info['bmWidth'], bmp_info['bmHeight']), bmp_str, 'raw', 'BGRX', 0, 1)

    # Cleanup
    dc.DeleteDC()
    compatible_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, window_dc)
    win32gui.DeleteObject(data_bit_map.GetHandle())

    return im


def is_matching_box(img, map_character_center, color, match_all=False, match_any=False, x_offset=0, y_offset=0, x_step=1, y_step=1, x_distance=14, y_distance=4):
    match = img.getpixel((map_character_center[0], map_character_center[1])) == color
    if not (match_all or match_any) and match:
        return match
    if match_all:
        for i in range(-x_distance, x_distance, x_step):
            if img.getpixel((map_character_center[0] + x_offset + i, map_character_center[1] + y_offset)) != color:
                return False
        for i in range(-y_distance, y_distance, y_step):
            if img.getpixel((map_character_center[0] + x_offset, map_character_center[1] + y_offset + i)) != color:
                return False
        return True
    if match_any:
        for i in range(-x_distance, x_distance, x_step):
            if img.getpixel((map_character_center[0] + x_offset + i, map_character_center[1] + y_offset)) == color:
                return True
        for i in range(-y_distance, y_distance, y_step):
            if img.getpixel((map_character_center[0] + x_offset, map_character_center[1] + y_offset + i)) == color:
                return True
        return False


def get_relative_map_and_enemy_set(img):
    relative_map = []
    enemy_set = set()
    obstacle_set = set()
    for _ in range(-scan_dist_x, scan_dist_x + 1, 1):
        relative_map.append([])
    for y in range(-scan_dist_y, scan_dist_y + 1, 1):
        for x in range(-scan_dist_x, scan_dist_x + 1, 1):
            world_cords = (x, y)
            map_pixel_coords = world_coords_to_pixel_coords(world_cords, map_character_center, max_box_pixel_translate)
            is_character = is_matching_box(img, map_pixel_coords, character_color, match_all=True)
            is_obstacle = (
                    is_matching_box(img, map_pixel_coords, obstacle_color, match_all=True, x_step=4, y_distance=0) or
                    is_matching_box(img, map_pixel_coords, obstacle_color, match_all=True, x_step=4, x_offset=2, y_distance=0)
                ) and (
                    is_matching_box(img, map_pixel_coords, obstacle_color, match_all=True, y_step=8, x_distance=0) or
                    is_matching_box(img, map_pixel_coords, obstacle_color, match_all=True, y_step=8, y_offset=2, x_distance=0) or
                    is_matching_box(img, map_pixel_coords, obstacle_color, match_all=True, y_step=8, y_offset=-2, x_distance=0)
            )
            is_enemy = is_matching_box(img, map_pixel_coords, enemy_color, match_all=True)
            relative_map[x].append((is_character, is_obstacle, is_enemy))
            if is_obstacle:
                obstacle_set.add((x, y))
            if is_enemy:
                enemy_set.add((x, y))

    return relative_map, enemy_set, obstacle_set
