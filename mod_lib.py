import random

player_default_params = {
    'health': 100,
    'max-health': 100,
    'damage': 6,  # use in range like: choice(range(damage - 10, damage))
    'armor': 0,
    'coins': 0,
    'inventory': [None for i in range(15)],
}

enemy_default_params = {
    'health': 10,
    'damage': lambda: random.randint(0, 3),
    'armor': 5,
    'coins': 10,
}

hard_enemy_default_params = {
    'health': 60,
    'damage': lambda: random.randint(10, 35),
    'armor': 20,
    'coins': 250,
}

boss_default_params = {
    'health': 200,
    'damage': lambda: random.randint(50, 100),
    'armor': 100,
    'coins': 1000,
}

params = {
    'grass': 'data/grass.png',
    'rock': 'data/rock.png',
    'sand': 'data/sand.png',
    # TODO! FIND PLAYER AND ENEMIES TEXTURE
    'enemy': ['', enemy_default_params],
    'boss': ['', boss_default_params],
    'hard-enemy': ['', hard_enemy_default_params],
    'player': 'data/character.png',
    'water': 'data/water.png',
    # TODO! FIND PICS FOR PLANTS
    'plants': [],
    'sand-plants': [],
    'trees': [],
    'sand-trees': [],
    'shop-man': '',
}


# TODO! FIND ITEMS TEXTURES

items = {
    'health-poison': '',
    'armor': '',
    'sword': '',
    'health-increase-pill': '',
    'coins-chest': '',
}
