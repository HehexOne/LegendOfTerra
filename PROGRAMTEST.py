import random
import sys
import os
import math
from PIL import Image, ImageFilter, ImageEnhance
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtGui import QPixmap


class Generate(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)

        self.water = 0
        self.grass = 1
        self.sand = 2
        self.snow = 3

        self.btn.clicked.connect(self.generate_map)

    def generate_map(self):
        self.size = int(self.square.text())
        self.water_barrier = int(self.ocean.text())
        self.grass_barrier = int(self.trava.text())
        print("\n\n----GENERATING ON----")
        img = Image.new("RGB", (self.size, self.size), (0, 0, 0))
        pixels = img.load()
        print("  Generating noise.")
        for x in range(0, self.size):
            for y in range(self.size):
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
        arr = [[0 for j in range(self.size)] for i in range(self.size)]
        snow_enabled = random.choice([0, 1])
        for x in range(0, self.size):
            for y in range(self.size):
                if self.grass_barrier < pixels[x, y][0]:
                    arr[x][y] = self.grass
                    pixels[x, y] = 0, random.randint(60, 160), 0
                elif pixels[x, y][0] < self.water_barrier:
                    arr[x][y] = self.water
                    pixels[x, y] = 30, 30, random.randint(60, 180)
                else:
                    arr[x][y] = self.sand
                    pixels[x, y] = random.randint(210, 240), \
                                   random.randint(160, 211), \
                                   random.randint(40, 95)
                if arr[x][y] != self.water and arr[x][y] != self.sand and \
                        math.degrees(random.uniform(0, 40) // 14) \
                        // 10 == snow_enabled:
                    arr[x][y] = self.snow
                    pixels[x, y] = random.randint(220, 255), \
                                   random.randint(220, 255), 255
        img.save('data/map.png')
        img.close()
        print("----GENERATED MAP----\n\n")


app = QApplication(sys.argv)
ex = Generate("")
ex.show()
sys.exit(app.exec_())