import pygame
from LegendOfTerra.mod_lib import *

pygame.init()
screen = pygame.display.set_mode(screen_size)

fps = 60
clock = pygame.time.Clock()

dp = DataProvider()
if dp.get_value("isNew"):
    generate_map()


pos = [0, 0]
world_map = dp.get_value("map")


tile_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
creatures_group = pygame.sprite.Group()

player = Player(creatures_group, 9, 4, 0, 0)


def init():
    pass


def start_screen():
    pass


def loading():
    pass


def game():
    for x in range(width // tile_size):
        for y in range(height // tile_size):
            tile = Tile(tile_group, world_map[pos[0]][pos[1]][y][x],
                        x * tile_size, y * tile_size)
            if not tile.kind:
                tile.add(water_group)


def pause():
    pass


running = True
game()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    player.move()
    clock.tick(fps)
    tile_group.draw(screen)
    creatures_group.draw(screen)
    creatures_group.update()
    pygame.display.flip()

pygame.quit()
