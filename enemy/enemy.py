import pygame

from functions import load_image


class Enemy(pygame.sprite.Sprite):
    def __init__(self, hp, x, y, enemy_group, all_sprites):
        super().__init__(enemy_group, all_sprites)

        self.hp = hp
        self.move_x, self.move_y = 0, 0

        self.speed = 1

        self.image = pygame.Surface((20, 20))
        self.image.fill('green')
        self.rect = self.image.get_rect().move(x, y)

        self.enemy_x, self.enemy_y = x, y

    def update(self):
        self.enemy_x, self.enemy_y = self.rect.x + self.speed * self.move_x, \
                                     self.rect.y + self.speed * self.move_y / self.koeff_x_to_y
        self.rect.x, self.rect.y = self.enemy_x, self.enemy_y

        if self.hp <= 0:
            self.kill()

    def move_to_player(self, player_pos):
        pos = (self.rect.x, self.rect.y)
        print(player_pos)
        try:
            self.move_x = -(pos[0] - player_pos.x) / abs(pos[0] - player_pos.x)
        except ZeroDivisionError:
            self.move_x = -1
        try:
            self.move_y = -(pos[1] - player_pos.y) / abs(pos[1] - player_pos.y)
        except ZeroDivisionError:
            self.move_y = -1
        self.koeff_x_to_y = abs(pos[0] - player_pos.x) / abs(pos[1] - player_pos.y)
        if self.koeff_x_to_y < 1:
            self.speed /= 1 / self.koeff_x_to_y

        self.move_x = -self.move_x
        self.move_y = - self.move_y

    def hit(self, damage):
        self.hp -= damage
