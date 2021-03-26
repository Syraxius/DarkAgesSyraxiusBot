import time
import random
import win32api
import win32con

from utils.pixel import world_coords_to_pixel_coords
from utils.coords import get_manhattan_distance
from utils.input import mouse_click, keyboard_send_vk_as_scan_code


def keyboard_walk_direction(hwnd, direction):
    vk = {
        'up': win32con.VK_UP,
        'right': win32con.VK_RIGHT,
        'down': win32con.VK_DOWN,
        'left': win32con.VK_LEFT,
    }.get(direction)
    keyboard_send_vk_as_scan_code(hwnd, vk, extended=1)


def keyboard_use_spell(hwnd, slot):
    vks = (
        win32con.VK_LMENU,  # Left Alt
        win32api.VkKeyScanEx('d', 0),  # Spells Tab
        win32api.VkKeyScanEx(str(slot), 0),
        win32api.VkKeyScanEx('g', 0),  # Char Tab
    )
    for vk in vks:
        keyboard_send_vk_as_scan_code(hwnd, vk)


def keyboard_use_skill(hwnd, slot):
    vks = (
        win32con.VK_LMENU,  # Left Alt
        win32api.VkKeyScanEx('s', 0),  # Skills Tab
        win32api.VkKeyScanEx(str(slot), 0),
        win32api.VkKeyScanEx('g', 0),  # Char Tab
    )
    for vk in vks:
        keyboard_send_vk_as_scan_code(hwnd, vk)


def keyboard_use_assail(hwnd):
    vks = (
        win32con.VK_LMENU,  # Left Alt
        win32con.VK_SPACE,  # Assail
    )
    for vk in vks:
        keyboard_send_vk_as_scan_code(hwnd, vk)


def keyboard_refresh(hwnd):
    vk = win32con.VK_F5
    keyboard_send_vk_as_scan_code(hwnd, vk)


def refresh(hwnd):
    keyboard_refresh(hwnd)
    time.sleep(1)


def use_spell_on_enemy(hwnd, spell_list, enemy, view_character_center, view_box_pixel_translate):
    spell_used = False
    for spell in spell_list:
        max_distance, slot, lines = spell
        is_enemy_in_range = get_manhattan_distance(enemy) < max_distance
        if is_enemy_in_range:
            print('Casting spell %s at %s' % (slot, enemy))
            enemy_view_pixel_coords = world_coords_to_pixel_coords(enemy, view_character_center, view_box_pixel_translate)
            keyboard_use_spell(hwnd, slot)
            mouse_click(hwnd, enemy_view_pixel_coords)
            time.sleep(lines + 0.1)
            refresh(hwnd)
            spell_used = True
            break
    return spell_used


def assail_enemy(hwnd, enemy):
    assailed = False
    is_enemy_in_range = get_manhattan_distance(enemy) == 1

    if is_enemy_in_range:
        direction_obs = {
            (0, -1): 'up',
            (1, 0): 'right',
            (0, 1): 'down',
            (-1, 0): 'left',
        }
        walk(hwnd, direction_obs[enemy], set())
        print('Using assail at %s' % (enemy,))
        keyboard_use_assail(hwnd)
        assailed = True
    return assailed


last_direction = None


def walk(hwnd, direction, obstacle_set):
    global last_direction

    direction_obs = {
        'up': (0, -1),
        'right': (1, 0),
        'down': (0, 1),
        'left': (-1, 0)
    }

    if direction_obs[direction] in obstacle_set:
        print('Blocked, picking random direction')
        direction = random.sample(['up', 'down', 'left', 'right'], 1)[0]

    if direction != last_direction:
        keyboard_walk_direction(hwnd, direction)
        time.sleep(0.1)

    keyboard_walk_direction(hwnd, direction)
    time.sleep(0.5)

    last_direction = direction
