import pygame

from functions import load_image


class Enemy(pygame.sprite.Sprite):
    def __init__(self, hp, x, y, enemy_group, all_sprites):
        super().__init__(enemy_group, all_sprites)

        self.hp = hp
        self.move_x, self.move_y = 0, 0

        self.speedx = 1
        self.speedy = 1

        self.image = pygame.Surface((20, 20))
        self.image.fill('green')
        self.rect = self.image.get_rect().move(x, y)

    def update(self):
        self.rect.x += self.move_x
        self.rect.y += self.move_y
        if self.hp <= 0:
            self.kill()

    def move_to_player(self, entity):
        entityx, entityy = entity.rect.x, entity.rect.y
        delta_x, delta_y = entityx - self.rect.x, entityy - self.rect.y
        S = ((self.rect.x - entityx) ** 2 + (self.rect.y - entityx) ** 2) ** (1 / 2)
        self.move_x, self.move_y = delta_x / S * self.speedx, delta_y / S * self.speedy

    def hit(self, damage):
        self.hp -= damage