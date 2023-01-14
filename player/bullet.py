import random

import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, moving_objects_group, player, pos):
        super().__init__(moving_objects_group)
        self.player = player
        player_pos = player.rect
        self.speed = 20
        self.damage = player.damage
        self.uses = 1
        self.pos = pygame.Vector2(player_pos.center[0], player_pos.center[1])
        self.delta_vector = pygame.Vector2(pos[0] - player_pos.center[0], pos[1] - player_pos.center[1])
        self.vector_len = self.delta_vector.length()
        if self.vector_len > 0:
            self.pos += self.delta_vector / self.vector_len * self.speed

        self.image = pygame.Surface((10, 10))
        self.image.fill('white')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos.x, self.pos.y

    def update(self, enemy_group):
        if self.rect.x >= 1500 or self.rect.y >= 1000:  # Через какое кол-во пикселей удаляется пуля
            self.kill()
        else:
            self.pos += self.delta_vector / self.vector_len * self.speed
            self.rect.x, self.rect.y = self.pos.x, self.pos.y
            for enemy in enemy_group:
                if self.rect.colliderect(enemy.rect):
                    enemy.hit(self.damage)
                    self.uses -= 1
                    if self.player.frozen:
                        a = random.randint(1, 100)
                        if a <= 50:
                            enemy.frozen = True, enemy.cur_frame
                    if self.uses == 0:
                        self.kill()
