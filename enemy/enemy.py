import pygame

from functions import load_image


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_group, all_sprites):
        super().__init__(enemy_group, all_sprites)

        self.move_x, self.move_y = 0, 0

        self.speedx = 3
        self.speedy = 3

        self.image = pygame.Surface((20, 20))
        self.image.fill('green')
        self.rect = self.image.get_rect().move(x, y)

    def update(self):
        self.rect.x += self.move_x
        self.rect.y += self.move_y

    def move_to_player(self, entity):
        entityx, entityy = entity.rect.x, entity.rect.y
        delta_x, delta_y = entityx - self.rect.x, entityy - self.rect.y
        S = ((self.rect.x - entityx) ** 2 + (self.rect.y - entityx) ** 2) ** (1 / 2)
        self.move_x, self.move_y = delta_x / S, delta_y / S
        print(self.move_x ,self.move_y)

