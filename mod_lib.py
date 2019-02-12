import random
import pygame
import json
import math
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
import os

tile_size = 225
fps = 60
screen_size = width, height = tile_size * 3, tile_size * 3


# High values of this parameter
#  Not recommended if you have got not so powerful PC (64 max)
size = 66  # Size of map (Example: size = 256  =>  map: 256x256)

# ID's for our map array which goes to save.json (For future comparing)
water = 0
grass = 1
sand = 2
snow = 3

# Min value is 0 and max value is 255
water_barrier = 100  # Standard values: 70
grass_barrier = 140  # Standard values: 140

block = [0, 0]


def get_block():
    global block
    return block


def set_block(val):
    global block
    block = val


textures = {
    0: "water.png",
    1: "grass.png",
    2: "sand.png",
    3: "snow.png"
}


# All groups
tile_group = pygame.sprite.Group()
creatures_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
borders = pygame.sprite.Group()
player_group = pygame.sprite.Group()
raccoons_group = pygame.sprite.Group()


# Reset saves.json
# Delete all saves
def reset():
    js = {"isNew": True}
    json.dump(js, open("data/save.json", 'w'))


# Custom function for load images
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def set_val(x, y, val, arr):
    tmp_val = width // tile_size
    arr[x // tmp_val][y // tmp_val][x % tmp_val][y % tmp_val] = val


# Function that generates the world and sets "isNew" variable to False
def generate_map():
    print("\n\n----GENERATING ON----")
    img = Image.new("RGB", (size, size), (0, 0, 0))
    pixels = img.load()
    print("  Generating noise.")
    for x in range(0, size):
        for y in range(size):
            # Difficult formula for generation
            val = int((random.uniform(0, 6.5) * 50) *
                      math.pi /
                      math.sin(random.uniform(0, 10)) *
                      math.cos(math.sqrt(2.1)))
            if val < 100:
                pixel = 0
            else:
                pixel = 255
            pixels[x, y] = pixel, 0, 0
    print("  Generated noise!!")
    img = img.filter(ImageFilter.GaussianBlur(1))
    img = ImageEnhance.Contrast(img).enhance(3)
    print(" Getting enhancement")
    pixels = img.load()
    print("    Few seconds..")
    tmp_val = width // tile_size
    arr = np.zeros((size // tmp_val, size // tmp_val, tmp_val, tmp_val),
                   dtype=np.int32)
    creatures = []
    snow_disabled = random.choice([0, 1])
    for x in range(size):
        for y in range(size):
            if grass_barrier < pixels[x, y][0]:
                set_val(x, y, grass, arr)
                pixels[x, y] = 0, random.randint(60, 160), 0
            elif pixels[x, y][0] < water_barrier:
                set_val(x, y, water, arr)
                pixels[x, y] = 30, 30, random.randint(60, 180)
            else:
                set_val(x, y, sand, arr)
                pixels[x, y] = random.randint(210, 240), \
                               random.randint(160, 211), \
                               random.randint(40, 95)
            if arr[x // tmp_val][y // tmp_val][x % tmp_val][y % tmp_val]\
                    != water and arr[x // tmp_val][y // tmp_val]\
                [x % tmp_val][y % tmp_val] != sand and \
                    math.degrees(random.uniform(0, 40) // 14) \
                    // 10 == snow_disabled:
                arr[x // tmp_val][y // tmp_val][x % tmp_val][y % tmp_val]\
                    = snow
                pixels[x, y] = random.randint(220, 255), \
                               random.randint(220, 255), 255
    for i in range(random.randint(20, 50)):
        creatures.append(Raccoon().generate_save())
    img.save("data/map.png")
    img.close()
    js = json.load(open("data/save.json", 'r'))
    js["creatures"] = creatures
    js["map"] = arr.tolist()
    json.dump(js, open("data/save.json", 'w'))
    print("----GENERATED MAP----\n\n")


class DataProvider:

    def __init__(self):
        try:
            self.data = json.load(open("data/save.json", 'r'))
        except Exception:
            reset()
            self.data = json.load(open("data/save.json", 'r'))

    def get_value(self, name):
        return self.data.get(name, None)

    def set_value(self, name, val):
        self.data[name] = val

    def save(self):
        self.data["isNew"] = False
        json.dump(self.data, open("data/save.json", 'w'))


class Creature(pygame.sprite.Sprite):

    def __init__(self, group, name, hp, damage, damage_delta):
        super().__init__(group)
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.damage = damage
        self.damage_delta = damage_delta
        self.get_damage = lambda: random.randint(
            self.damage - self.damage_delta,
            self.damage)
        self.coins = 0
        self.speed = 4
        # self.image = load_image(image)
        # self.rect = self.image.get_rect()
        # self.rect.x = 0
        # self.rect.y = 0
        self.side = 0

    def cast_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()
            del self


class Player(Creature):

    def __init__(self, group, columns, rows, x, y):
        super().__init__(group, "Player", 10, 10, 9)
        self.frames = []
        self.cut_sheet(load_image('player.png'), columns, rows)
        self.cur_frame = 24
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.num_of_potions = 3
        self.score = 0

    def restore_from_save(self, d):
        self.name = d["name"]
        self.hp = d["hp"]
        self.max_hp = d["max_hp"]
        self.damage = d["damage"]
        self.damage_delta = d["damage_delta"]
        self.get_damage = lambda: random.randint(
            self.damage - self.damage_delta,
            self.damage)
        self.coins = d["coins"]
        self.rect.x = d["coords"]["x"]
        self.rect.y = d["coords"]["y"]
        self.score = d["score"]
        self.num_of_potions = d["num_of_potions"]
        while pygame.sprite.spritecollideany(self, water_group):
            self.rect.x = random.randint(1, d["coords"]["x"])
            self.rect.y = random.randint(1, d["coords"]["y"])

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def use_potion(self):
        if self.num_of_potions != 0:
            self.num_of_potions -= 1
            self.max_hp += 10
            self.hp = self.max_hp

    def update(self, world_map):
        old_x = self.rect.x
        old_y = self.rect.y
        if pygame.key.get_pressed()[pygame.K_UP]:
            new_x = 0
            new_y = -self.speed
            self.image = self.frames[random.randint(0, 8)]
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            new_x = 0
            new_y = self.speed
            self.image = self.frames[random.randint(18, 26)]
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            new_x = -self.speed
            new_y = 0
            self.image = self.frames[random.randint(9, 17)]
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            new_x = self.speed
            new_y = 0
            self.image = self.frames[random.randint(27, 33)]
        else:
            new_x = 0
            new_y = 0
        self.rect = self.rect.move(new_x, new_y)
        if pygame.sprite.spritecollideany(self, water_group):
            self.rect = self.rect.move(old_x - self.rect.x, old_y - self.rect.y)
        brds = pygame.sprite.spritecollideany(self, borders)
        if brds:
            global block
            tmp_block = block
            self.rect = self.rect.move(old_x - self.rect.x, old_y - self.rect.y)
            x, y = self.rect.x, self.rect.y
            if brds.type == "up" and block[1] != 0:
                self.move(self.rect.x, 580)
                block = [block[0], block[1] - 1]
            elif brds.type == "down" and block[1] != (size // (width // tile_size)) - 1:
                self.move(self.rect.x, 10)
                block = [block[0], block[1] + 1]
            elif brds.type == "left" and block[0] != 0:
                self.move(580, self.rect.y)
                block = [block[0] - 1, block[1]]
            elif brds.type == "right" and block[0] != (size // (width // tile_size)) - 1:
                self.move(20, self.rect.y)
                block = [block[0] + 1, block[1]]
            re_render(world_map)
            if pygame.sprite.spritecollideany(self, water_group):
                self.move(x, y)
                block = tmp_block
                re_render(world_map)

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def generate_save(self):
        return {"name": self.name,
                "hp": self.hp,
                "max_hp": self.max_hp,
                "damage": self.damage,
                "damage_delta": self.damage_delta,
                "coins": self.coins,
                "coords": {"x": self.rect.x,
                           "y": self.rect.y},
                "score": self.score,
                "num_of_potions": self.num_of_potions}


class Raccoon(Creature):

    def __init__(self, d=None):
        super().__init__(creatures_group, "Shop", 2 ** 45, 0, 0)
        self.block = [random.randint(0, 21), random.randint(0, 21)]
        self.frames = []
        self.add(raccoons_group)
        self.removed = False
        self.cut_sheet(load_image('raccoon.png'), 12, 8)
        self.cur_frame = 58
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(random.randint(20, width - 30), random.randint(20, width - 30))
        if d is not None:
            self.restore_from_save(d)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, world_map):
        if pygame.sprite.spritecollideany(self, water_group):
            self.remove(creatures_group)
            return
        if not self.removed and block != self.block:
            self.remove(creatures_group)
            self.removed = True
        elif self.removed and block == self.block:
            self.add(creatures_group)
            self.removed = False
        player = pygame.sprite.spritecollideany(self, player_group)
        if player and pygame.key.get_pressed()[pygame.K_e] and player.coins >= 100:
            player.coins -= 100
            player.num_of_potions += 1

    def generate_save(self):
        return {"type": "Raccoon",
                "coords": {
                    "block": self.block,
                    "coords": [self.rect.x, self.rect.y]
                }
                }

    def restore_from_save(self, d):
        self.block = d["coords"]["block"]
        self.rect.x = d["coords"]["coords"][0]
        self.rect.y = d["coords"]["coords"][1]


class Tile(pygame.sprite.Sprite):

    def __init__(self, group, kind, x, y):
        super().__init__(group)
        self.kind = kind
        self.image = load_image(textures[kind])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def re_render(world_map):
    [i.kill() for i in tile_group.sprites()]
    for x in range(width // tile_size):
        for y in range(height // tile_size):
            tile = Tile(tile_group, world_map[block[0]][block[1]][x][y],
                        x * tile_size, y * tile_size)
            if not tile.kind:
                tile.add(water_group)


class Border(pygame.sprite.Sprite):

    def __init__(self, x1, y1, x2, y2, type):
        super().__init__(all_sprites)
        self.add(borders)
        self.type = type
        if x1 == x2:
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
