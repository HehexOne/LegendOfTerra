import pygame
import mod_lib

pygame.init()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)

pygame.display.flip()

running = True

fps = 60
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(fps)
    pygame.display.flip()

pygame.quit()
