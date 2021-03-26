import ctypes
import win32process
from configs.memory import pointer_values, map_data_base, map_data_offsets


def get_static_object_tile_pass():
    sotp = []
    with open('sotp.dat', 'rb') as f:
        next_byte = f.read(1)
        while next_byte != b'':
            sotp.append(ord(next_byte))
            next_byte = f.read(1)
    return sotp


def get_all_memory_values(hwnd, sotp):
    process_vm_read = 0x0010  # Permission
    pid = win32process.GetWindowThreadProcessId(hwnd)[1]
    handle = ctypes.windll.kernel32.OpenProcess(process_vm_read, False, pid)

    # Get normal data

    buffer = ctypes.c_uint32()
    buffer_length = 4
    memory_values = {}
    for pointer_value in pointer_values:
        base_pointer = pointer_values[pointer_value]['base']
        ctypes.windll.kernel32.ReadProcessMemory(handle, base_pointer, ctypes.byref(buffer), buffer_length, None)
        curr_value = buffer.value
        for offset in pointer_values[pointer_value]['offsets']:
            ctypes.windll.kernel32.ReadProcessMemory(handle, curr_value + offset, ctypes.byref(buffer), buffer_length, None)
            curr_value = buffer.value
        memory_values[pointer_value] = curr_value

    base_pointer = map_data_base
    for offset in map_data_offsets:
        ctypes.windll.kernel32.ReadProcessMemory(handle, base_pointer, ctypes.byref(buffer), buffer_length, None)
        base_pointer = buffer.value + offset

    offset = 0
    buffer = ctypes.c_uint16()
    buffer_length = 2
    obstacle_set = set()
    for y in range(memory_values['size_y']):
        for x in range(memory_values['size_x']):
            offset += 1
            ctypes.windll.kernel32.ReadProcessMemory(handle, base_pointer + 2 * offset, ctypes.byref(buffer), buffer_length, None)
            wall1 = buffer.value
            offset += 1
            ctypes.windll.kernel32.ReadProcessMemory(handle, base_pointer + 2 * offset, ctypes.byref(buffer), buffer_length, None)
            wall2 = buffer.value
            offset += 1

            is_wall = False
            if wall1 != 0:
                is_wall = sotp[wall1 - 1] & 0x0F == 0x0F
            elif wall2 != 0:
                is_wall = sotp[wall2 - 1] & 0x0F == 0x0F
            if is_wall:
                obstacle_set.add((x, y))

    memory_values['obstacle_set'] = obstacle_set

    obstacle_set_rel = set()
    for obstacle in obstacle_set:
        obstacle_set_rel.add((obstacle[0] - memory_values['pos_x'], obstacle[1] - memory_values['pos_y']))
    memory_values['obstacle_set_rel'] = obstacle_set_rel

    ctypes.windll.kernel32.CloseHandle(handle)
    return memory_values
