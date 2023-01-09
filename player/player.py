import pygame

from functions import load_image


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, player_group, all_sprites):
        super().__init__(player_group, all_sprites)
        self.player_x, self.player_y = x, y
        self.frames = []
        self.cut_sheet(load_image('resourses/sprites/player.png', -1), 6, 11)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale2x(self.image)
        self.speedx = 5
        self.speedy = 5
        self.rect = self.image.get_rect().move(x, y)  # Координаты спавна персонажа

    def apply_changes(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

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
