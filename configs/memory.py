pointer_values = {
    # To find the map target address, go to each map and scan for the map number according to the waypoint list above.
    'map': {
        'base': 0x00882E68,
        'offsets': (0x26C,)
    },
    # To find HP and MP target address, scan for HP and MP directly.
    'hp': {
        'base': 0x00882E68,
        'offsets': (0x2CC, 0x1078)
    },
    'mp': {
        'base': 0x00882E68,
        'offsets': (0x2CC, 0x1080)
    },
    # To find size_x and size_y target address, scan for pos_x and pos_y first, then work backwards.
    'size_x': {
        'base': 0x00884A74,
        'offsets': (0x20C, 0x0)
    },
    'size_y': {
        'base': 0x00884A74,
        'offsets': (0x20C, 0x4)
    },
    'pos_x': {
        'base': 0x00884A74,
        'offsets': (0x20C, 0x20)
    },
    'pos_y': {
        'base': 0x00884A74,
        'offsets': (0x20C, 0x1C)
    }
}

# To find the map data target address, scan 8-byte value 78532291608117526 at Crypt 2-1.
map_data_base = 0x00882E68
map_data_offsets = (0x27C, 0xC, 0x0)
