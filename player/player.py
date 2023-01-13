import pygame

from functions import load_image, cut_sheet


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, hp, x, y, player_group, all_sprites):
        super().__init__(player_group, all_sprites)
        self.player_x, self.player_y = x, y
        self.frames = []
        self.hp = [hp, hp]
        cut_sheet(self, load_image('resourses/sprites/player/player.png', -1), 6, 11)
        self.cur_frame = 0
        self.last_hit = 0
        self.percentage = self.hp[0] / self.hp[1]
        self.shot_speed = 90  # Выстрелов в минуту
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale2x(self.image)
        self.mask = pygame.mask.from_surface(self.image)
        self.speedx = 5
        self.speedy = 5
        self.rect = self.image.get_rect().move(x, y)  # Координаты спавна персонажа

    def apply_changes(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def update_hp_bar(self, screen):
        pygame.draw.rect(screen, 'gray', (80, 50, 240, 20), border_radius=10)
        pygame.draw.rect(screen, 'red', (80, 50, 240 * self.percentage, 20),
                         border_radius=10)
        print(self.hp)

    def update(self, screen, left, right, up, down, enemy_group):
        if self.cur_frame - self.last_hit > 30:
            if pygame.sprite.spritecollideany(self, enemy_group):
                self.hp[0] -= 10
            self.last_hit = self.cur_frame
            try:
                self.percentage = self.hp[0] / self.hp[1]
            except ZeroDivisionError:
                self.percentage = 0
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
        self.cur_frame += 1
