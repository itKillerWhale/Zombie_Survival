import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, moving_objects_group, player_pos, pos):
        super().__init__(moving_objects_group)
        self.speed = 20
        self.damage = 10
        self.uses = 1
        self.bullet_x, self.bullet_y = player_pos.center[0], player_pos.center[1]
        try:
            self.move_x = (pos[0] - player_pos.center[0]) / abs(pos[0] - player_pos.center[0])
        except ZeroDivisionError:
            self.move_x = 1
        try:
            self.move_y = (pos[1] - player_pos.center[1]) / abs(pos[1] - player_pos.center[1])
        except ZeroDivisionError:
            self.move_y = 1
        self.koeff_x_to_y = abs(pos[0] - player_pos.center[0]) / abs(pos[1] - player_pos.center[1])
        if self.koeff_x_to_y < 1:
            self.speed /= 1 / self.koeff_x_to_y
        self.image = pygame.Surface((10, 10))
        self.image.fill('white')
        self.rect = self.image.get_rect().move(player_pos.center[0], player_pos.center[1])

    def update(self, enemy_group):
        if self.rect.x >= 1500 or self.rect.y >= 1000:  # Через какое кол-во пикселей удаляется пуля
            self.image = pygame.Surface((10, 10))
            self.rect.x, self.rect.y = 5000, 5000
        else:
            self.bullet_x, self.bullet_y = self.bullet_x + self.speed * self.move_x, \
                                           self.bullet_y + self.speed * self.move_y / self.koeff_x_to_y
            self.rect.x, self.rect.y = self.bullet_x, self.bullet_y
            for enemy in enemy_group:
                if self.rect.colliderect(enemy.rect):
                    enemy.hit(self.damage)
                    self.uses -= 1
                    if self.uses == 0:
                        self.kill()
