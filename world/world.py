import pygame
import random

from functions import load_image


class Tile(pygame.sprite.Sprite):
    kind_of_tiles = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2]

    def __init__(self, x, y, tiles_group, all_sprites):
        super().__init__(tiles_group, all_sprites)

        self.image = pygame.Surface((80, 80))
        self.generate()
        self.rect = self.image.get_rect().move(x, y)

    def update(self, player_pos):
        if player_pos.x - self.rect.x >= 710:
            self.rect.x += 1280 + 80
            self.generate()

        elif player_pos.x - self.rect.x <= - 650:
            self.rect.x -= 1280 + 80
            self.generate()

        elif player_pos.y - self.rect.y >= 430:
            self.rect.y += 720 + 80
            self.generate()

        elif player_pos.y - self.rect.y <= -370:
            self.rect.y -= 720 + 80
            self.generate()

    def generate(self):
        kind = random.choice(Tile.kind_of_tiles)
        if kind == 0:
            self.image.fill('blue')
        if kind == 1:
            self.image.fill('black')
        if kind == 2:
            self.image.fill('red')


# class World(pygame.sprite.Sprite):
#     def __init__(self, height, width, world_group, all_sprites):
#         super().__init__(world_group, all_sprites)
