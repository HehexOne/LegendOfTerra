import pygame
from mod_lib import *

pygame.init()
screen = pygame.display.set_mode(screen_size)

fps = 60
clock = pygame.time.Clock()

dp = DataProvider()
if dp.get_value("isNew"):
    generate_map()

tile_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
creatures_group = pygame.sprite.Group()


def init():
    pass


def start_screen():
    pass


def loading():
    pass


def game():
    screen.blit(pygame.transform.scale(load_image("map.png"), (size * tile_size, size * tile_size)), (0, 0))
    Player(creatures_group, 9, 4, 0, 0)


def pause():
    pass


running = True
game()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(fps)
    screen.blit(pygame.transform.scale(load_image("map.png"), (size * tile_size, size * tile_size)), (0, 0))
    creatures_group.draw(screen)
    creatures_group.update()
    tile_group.draw(screen)
    pygame.display.flip()

pygame.quit()
