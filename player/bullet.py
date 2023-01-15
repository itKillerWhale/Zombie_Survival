import random
import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, moving_objects_group, player, pos, image):
        super().__init__(moving_objects_group)
        self.player = player
        player_pos = player.rect
        self.speed = 30
        self.damage = player.damage
        self.uses = player.bullet_pierces
        self.image = image
        self.main_vector = pygame.Vector2(10, 0)
        self.pos = pygame.Vector2(player_pos.center[0], player_pos.center[1])
        self.delta_vector = pygame.Vector2(pos[0] - player_pos.center[0], pos[1] - player_pos.center[1])
        self.vector_len = self.delta_vector.length()
        self.damaged = []
        if self.vector_len > 0:
            self.pos += self.delta_vector / self.vector_len * self.speed
        local_vector = self.delta_vector / self.vector_len * self.speed
        self.image = pygame.transform.rotate(self.image, local_vector.angle_to(self.main_vector))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos.x, self.pos.y

    def update(self, enemy_group):
        if self.rect.x >= 1500 or self.rect.y >= 1000:  # Через какое кол-во пикселей удаляется пуля
            self.kill()
        else:
            self.pos += self.delta_vector / self.vector_len * self.speed
            self.rect.x, self.rect.y = self.pos.x, self.pos.y
            for enemy in enemy_group:
                if self.rect.colliderect(enemy.rect) and enemy not in self.damaged:
                    enemy.hit(self.damage)
                    self.damaged.append(enemy)
                    self.uses -= 1
                    if self.player.frozen[0]:
                        a = random.randint(1, 100)
                        if a <= 20:
                            enemy.frozen = True, enemy.cur_frame
                    if self.uses == 0:
                        self.kill()
