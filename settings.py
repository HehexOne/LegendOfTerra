import mod_lib
import pygame


class Item(pygame.sprite.Sprite):

    def __init__(self, group, item_name):
        super().__init__(group)
        self.image = mod_lib.params[item_name]
        self.rect = self.image.get_rect()


class Enemy(pygame.sprite.Sprite):

    def __init__(self, group, enemy):
        super().__init__(group)
        self.image = mod_lib.params[enemy][0]
        self.params = mod_lib.params[enemy][1].copy()
        self.rect = self.image.get_rect()

    def cast_damage(self, other):
        other.params['health'] -= self.params['damage']()
        if other['health'] <= 0:
            other.destroy()

    def destroy(self):
        del self
