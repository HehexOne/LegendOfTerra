import random


texture = {
    'grass': 'data/grass.png',
    'rock': 'data/rock.png',
    'sand': 'data/sand.png',
    # TODO! FIND PLAYER AND ENEMIES TEXTURE
    'enemy': '',
    'boss': '',
    'hard-enemy': '',
    'player': 'data/character.png',
    'water': 'data/water.png',
    # TODO! FIND PICS FOR PLANTS
    'plants': [],
    'sand-plants': [],
    'trees': [],
    'sand-trees': [],
}

player_default_params = {
    'health': 100,
    'max-health': 100,
    'damage': lambda: random.randint(1, 6),
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
    'armor': 20,
    'coins': 250,
}


# TODO! FIND ITEMS TEXTURES

items = {
    'health-poison': '',
    'armor': '',
    'sword': '',
    'health-increase-pill': '',
}
