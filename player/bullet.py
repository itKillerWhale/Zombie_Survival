import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, moving_objects_group, player_rect, pos):
        super().__init__(moving_objects_group)
        self.speed = 20
        self.bullet_x, self.bullet_y = player_rect.x, player_rect.y
        try:
            self.move_x = (pos[0] - player_rect.x) / abs(pos[0] - player_rect.x)
        except ZeroDivisionError:
            self.move_x = 1
        try:
            self.move_y = (pos[1] - player_rect.y) / abs(pos[1] - player_rect.y)
        except ZeroDivisionError:
            self.move_y = 1
        self.koeff_x_to_y = abs(pos[0] - player_rect.x) / abs(pos[1] - player_rect.y)
        if self.koeff_x_to_y < 1:
            self.speed /= 1 / self.koeff_x_to_y
        self.image = pygame.Surface((10, 10))
        self.image.fill('white')
        self.rect = self.image.get_rect().move(player_rect.x, player_rect.y)

    def update(self):
        if self.rect.x >= 1500 or self.rect.y >= 1000:  # Через какое кол-во пикселей удаляется пуля
            self.image = pygame.Surface((10, 10))
            self.rect.x, self.rect.y = 1500, 1500
        else:
            self.bullet_x, self.bullet_y = self.bullet_x + self.speed * self.move_x, \
                                           self.bullet_y + self.speed * self.move_y / self.koeff_x_to_y
            self.rect.x, self.rect.y = self.bullet_x, self.bullet_y