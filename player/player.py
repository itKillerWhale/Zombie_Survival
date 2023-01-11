import pygame

from functions import load_image, cut_sheet


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, player_group, all_sprites):
        super().__init__(player_group, all_sprites)
        self.player_x, self.player_y = x, y
        self.frames = []
        cut_sheet(self, load_image('resourses/sprites/player/player.png', -1), 6, 11)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale2x(self.image)
        self.mask = pygame.mask.from_surface(self.image)
        self.speedx = 5
        self.speedy = 5
        self.rect = self.image.get_rect().move(x, y)  # Координаты спавна персонажа

    def apply_changes(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def update(self, left, right, up, down):
        if left:
            self.rect.x += -self.speedx
            self.player_x += -self.speedx
        if right:
            self.rect.x += self.speedx
            self.player_x += self.speedx
        if up:
            self.rect.y += -self.speedy
            self.player_y += -self.speedy
        if down:
            self.rect.y += self.speedy
            self.player_y += self.speedy
