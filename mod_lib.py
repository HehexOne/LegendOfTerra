import random
import pygame
import json
import math
from PIL import Image, ImageFilter, ImageEnhance

fps = 60

# High values of this parameter not recommended if you have got not so powerful PC (64 max)
size = 64  # Size of map (Example: size = 256  =>  map: 256x256)


grass = 255
sand = 150
water = 0


# Min value is 0 and max value is 255
water_barrier = 70  # 70
grass_barrier = 170  # 170


def reset():
    js = {"isNew": True}
    json.dump(js, open("data/save.json", 'w'))


class SeedException(Exception):
    pass


def generate_map():
    img = Image.new("RGB", (size, size), (0, 0, 0))
    pixels = img.load()
    print("Generating noise")
    for x in range(0, size):
        for y in range(size):
            val = int((random.uniform(0, 5) * 50) * math.pi / math.sin(random.uniform(0, 10)) * math.cos(math.sqrt(2.1)))
            if val < 100:
                pixel = 0
            else:
                pixel = 255
            pixels[x, y] = pixel, 0, 0
    print("Generated noise!")
    img = img.filter(ImageFilter.GaussianBlur(1))
    img = ImageEnhance.Contrast(img).enhance(3)
    print("Getting enhancement")
    pixels = img.load()
    print("Few seconds...")
    arr = [[0 for j in range(size)] for i in range(size)]
    for x in range(0, size):
        for y in range(size):
            if grass_barrier < pixels[x, y][0]:
                arr[x][y] = 255
                pixels[x, y] = 0, 160, 0
            elif pixels[x, y][0] < water_barrier:
                arr[x][y] = 0
                pixels[x, y] = 0, 0, 160
            else:
                arr[x][y] = 150
                pixels[x, y] = 255, 211, 95
    img.save('map.png')
    img.close()
    js = json.load(open("data/save.json", 'r'))
    js["map"] = arr
    js["isNew"] = False
    json.dump(js, open("data/save.json", 'w'))
    print("----GENERATED MAP----")


class Creature:

    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.damage = damage
        self.get_damage = lambda: random.randint(1, self.damage)
        self.coins = 0

