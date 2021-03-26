map_waypoints = {
    500: {  # Mileth
        'is_home': True,
        'training_grounds_coords': (91, 54),
        'ignored_obstacles': [
            (91, 54)
        ]
    },
    425: {  # Crypt Vestibule
        'is_home': True,
        'training_grounds_coords': (8, 7)
    },
    1: {  # Crypt 1-1
        'virtual_obstacles': [
            (3, 4),
            (40, 45),
            (45, 17)
        ],
        'ignored_obstacles': [
            (18, 2)
        ]
    },
    2: {  # Crypt 2-1
        'virtual_obstacles': [
            (44, 22),
            (11, 23),
        ],
        'ignored_obstacles': [
            (9, 5)
        ]
    },
    3: {  # Crypt 2-2
        'virtual_obstacles': [
            (44, 1),
            (11, 23),
        ],
        'ignored_obstacles': [
            (9, 5)
        ],
        'patrol': [
            ((43, 43), 2),
            ((16, 39), 2),
            ((4, 41), 2),
            ((5, 6), 2),
            ((20, 6), 2),
            ((38, 3), 2),
        ],
    },
    5: {  # Crypt 3-1
        'patrol': [
            ((22, 9), 2),
            ((5, 5), 2),
            ((5, 27), 2),
            ((19, 19), 2),
            ((18, 44), 2),
            ((37, 39), 2),
            ((40, 24), 2),
            ((43, 6), 2),
        ],
        'virtual_obstacles': [
            (0, 30),
            (29, 45),
            (40, 2),
        ]
    },
    8: {  # Crypt 4-1
        'patrol': [
            ((5, 47), 2),
            ((14, 41), 2),
            ((6, 25), 2),
            ((25, 42), 2),
            ((41, 42), 2),
            ((20, 23), 2),
            ((44, 8), 2),
            ((6, 8), 2),
        ],
        'virtual_obstacles': [
            (5, 0),
            (5, 40),
        ]
    },
    9: {  # Crypt 4-2
        'patrol': [
            ((0, 0), 5),
            ((0, 49), 5),
            ((49, 49), 5),
            ((49, 0), 5),
            ((25, 25), 5),
        ],
        'virtual_obstacles': [
            (45, 1),
            (28, 33),
            (0, 39),
            (8, 0),
        ]
    },
    600: {  # East Woodland Crossroads
        'is_home': True,
        'rest': (21, 21),
        # 'training_grounds_coords': (3, 0),  # East Woodland 3-1
        'training_grounds_coords': (13, 0),  # East Woodland 5-1
    },
    622: {  # Enchanted Gardens
        'rest': (99, 49),  # East Woodland Crossroads
        'patrol': [
            ((90, 10), 10),
            ((10, 10), 10),
            ((10, 90), 10),
            ((90, 90), 10),
        ]
    },
    601: {  # East Woodland 3-1
        'rest': (25, 99),  # East Woodland Crossroads
        'patrol': [
            ((90, 10), 10),
            ((10, 10), 10),
            ((10, 90), 10),
            ((90, 90), 10),
        ]
    },
    603: {  # East Woodland 5-1
        'rest': (25, 99),  # East Woodland Crossroads
        'patrol': [
            ((90, 10), 10),
            ((10, 10), 10),
            ((10, 90), 10),
            ((90, 90), 10),
        ]
    },
    340: {  # Dubhaim Castle
        'training_grounds_coords': (12, 26),  # Dubhaim Castle West Corr
    },
    319: {  # Dubhaim Castle West Corr
        'is_home': True,
        'rest': (8, 20),
        'patrol': [
            # ((0, 2), 0),  # Dubhaim Castle West 6-1
            ((0, 8), 0),  # Dubhaim Castle West 5-1
            ((0, 14), 0),  # Dubhaim Castle West 4-1
            ((0, 20), 0),  # Dubhaim Castle West 3-1
            # ((0, 26), 0),  # Dubhaim Castle West 2-1
        ]
    },
    321: {  # Dubhaim Castle West 2-1
        'rest': (21, 11),  # Dubhaim Castle West Corr
        'patrol': [
            ((11, 11), 0),
            ((21, 11), 0)  # Dubhaim Castle West Corr
        ]
    },
    322: {  # Dubhaim Castle West 3-1
        'rest': (21, 11),  # Dubhaim Castle West Corr
        'patrol': [
            ((11, 11), 0),
            ((21, 11), 0)  # Dubhaim Castle West Corr
        ]
    },
    323: {  # Dubhaim Castle West 4-1
        'rest': (21, 11),  # Dubhaim Castle West Corr
        'patrol': [
            ((11, 11), 0),
            ((21, 11), 0)  # Dubhaim Castle West Corr
        ]
    },
    324: {  # Dubhaim Castle West 5-1
        'rest': (21, 11),  # Dubhaim Castle West Corr
        'patrol': [
            ((11, 11), 0),
            ((21, 11), 0)  # Dubhaim Castle West Corr
        ]
    },
    325: {  # Dubhaim Castle West 6-1
        'rest': (21, 11),  # Dubhaim Castle West Corr
        'patrol': [
            ((11, 11), 0),
            ((21, 11), 0)  # Dubhaim Castle West Corr
        ]
    },
    311: {  # Dubhaim Castle East
        'rest': (21, 11),  # Dubhaim Castle West Corr
        'patrol': [
            ((11, 11), 0),
        ]
    },
}
