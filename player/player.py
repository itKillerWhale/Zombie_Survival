import pygame

from functions import load_image


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, player_group, all_sprites):
        super().__init__(player_group, all_sprites)
        self.world_x, self.world_y = x, y
        self.speedx = 5
        self.speedy = 5
        self.image = pygame.Surface((20, 20))
        self.image.fill('red')
        self.rect = self.image.get_rect().move(x, y)  # Координаты спавна персонажа

    def update(self, left, right, up, down):
        if left:
            self.rect.x += -self.speedx
            self.world_x += -self.speedx
        if right:
            self.rect.x += self.speedx
            self.world_x += self.speedx
        if up:
            self.rect.y += -self.speedy
            self.world_y += -self.speedy
        if down:
            self.rect.y += self.speedy
            self.world_y += self.speedy
