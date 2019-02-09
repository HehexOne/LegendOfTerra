import random
import pygame
import json
import math
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
import os

fps = 60
screen_size = width, height = 900, 900
tile_size = 225

# High values of this parameter
#  Not recommended if you have got not so powerful PC (64 max)
size = 64  # Size of map (Example: size = 256  =>  map: 256x256)

# ID's for our map array which goes to save.json (For future comparing)
water = 0
grass = 1
sand = 2
snow = 3

# Min value is 0 and max value is 255
water_barrier = 100  # Standard values: 70
grass_barrier = 140  # Standard values: 140

textures = {
    0: "water.png",
    1: "grass.png",
    2: "sand.png",
    3: "snow.png"
}


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
    arr[x // tmp_val][y // tmp_val][y % tmp_val][x % tmp_val] = val


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
    img.save("data/map.png")
    img.close()
    js = json.load(open("data/save.json", 'r'))
    js["map"] = arr.tolist()
    js["isNew"] = False
    json.dump(js, open("data/save.json", 'w'))
    print("----GENERATED MAP----\n\n")


class DataProvider:

    def __init__(self):
        self.data = json.load(open("data/save.json", 'r'))

    def get_value(self, name):
        return self.data.get(name, None)

    def set_value(self, name, val):
        self.data[name] = val

    def save(self):
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
        self.speed = 20
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
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

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

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def generate_save(self):
        return {"name": self.name,
                "hp": self.hp,
                "max_hp": self.max_hp,
                "damage": self.damage,
                "damage_delta": self.damage_delta,
                "coins": self.coins,
                "coords": {"x": self.rect.x,
                           "y": self.rect.y}}


class Tile(pygame.sprite.Sprite):

    def __init__(self, group, kind, x, y):
        super().__init__(group)
        self.image = load_image(textures[kind])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

