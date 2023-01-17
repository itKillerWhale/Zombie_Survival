import copy
import math
import random

import pygame

FROZEN_ZOMBIE = pygame.image.load('resourses/sprites/zombie/Zombie_Frozen.png')
FROZEN_ZOMBIE_REVERSE = pygame.transform.flip(FROZEN_ZOMBIE, True, False)


# Класс для создания монстров
class Enemy(pygame.sprite.Sprite):
    def __init__(self, hp, x, y, image, enemy_group, all_sprites):
        super().__init__(enemy_group, all_sprites)

        self.hp = hp
        self.move_x, self.move_y = 0, 0

        self.speed = 3
        self.cur_frame = 0
        self.collide = None

        self.image = image
        self.frozen = False, 0
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(x, y)

        self.pos = pygame.Vector2(x, y)

    # Функция для смещения объекта
    def apply_changes(self, dx, dy):
        self.pos.x += dx
        self.pos.y += dy

    def update(self, player, game_difficult, image, image2, orbs_group, enemy_group, other_objects_group, all_sprites):
        player_pos = player.rect
        self.cur_frame += 1
        delta_vector = pygame.Vector2(player_pos.center[0] - 10, player_pos.center[1] + 10) - self.pos
        if math.hypot(player_pos.x - self.rect.x, player_pos.y - self.rect.y) < 900:
            if self.frozen[0] and self.cur_frame - self.frozen[1] <= 60:
                if delta_vector.x > 0:
                    self.image = FROZEN_ZOMBIE
                else:
                    self.image = FROZEN_ZOMBIE_REVERSE
            else:
                self.frozen = False, 0
                if delta_vector.x > 0:
                    self.image = image
                else:
                    self.image = image2
        self.speed = 3 + game_difficult // 5
        if not (3 <= int(self.cur_frame / (6 / (game_difficult // 5 + 3))) % 8 <= 6):
            vector_len = delta_vector.length()
            old_rect = copy.deepcopy(self.rect)
            old_pos = copy.deepcopy(self.pos)
            if vector_len > 0 and not self.frozen[0]:
                self.pos += delta_vector / vector_len * min(vector_len, self.speed)
                self.rect.x, self.rect.y = self.pos.x, self.pos.y
                if self.check(other_objects_group):
                    self.rect = old_rect
                    self.pos = old_pos
        self.rect.x, self.rect.y = self.pos.x, self.pos.y

        if self.hp <= 0:
            player.kills += 1
            if player.vampirizm:
                a = random.randint(1, 100)
                if a <= 5 and player.hp[0] < player.hp[1]:
                    player.hp[0] += 1
            enemy_group.remove(self)
            self.kill()
            ExpOrb(1, (self.rect.centerx, self.rect.centery), orbs_group, all_sprites)

        collides = pygame.sprite.spritecollide(self, enemy_group, False)
        if collides:
            for enemy in collides:
                if enemy != self and pygame.sprite.collide_mask(self, enemy):
                    enemy_pos = enemy.rect
                    delta_vector = pygame.Vector2(enemy_pos.center[0] - self.rect.centerx,
                                                  enemy_pos.center[1] - self.rect.centery)
                    vector_len = delta_vector.length()
                    if vector_len > 0:
                        self.pos -= delta_vector / vector_len * min(vector_len, self.speed)

        if self.collide is not None:
            if math.hypot(self.collide.rect.centerx - player.rect.centerx,
                          self.collide.rect.centery - player.rect.centery) - math.hypot(
                self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery) <= 0:
                delta_vector = pygame.Vector2(player_pos.center[0] - 10, player_pos.center[1] + 10) - self.pos
                vector_len = delta_vector.length()
                self.pos -= delta_vector.rotate(90) / vector_len * min(vector_len, self.speed)
            else:
                delta_vector = pygame.Vector2(player_pos.center[0] - 10, player_pos.center[1] + 10) - self.pos
                vector_len = delta_vector.length()
                self.pos -= delta_vector / vector_len * min(vector_len, self.speed) * 2
        self.collide = None
        self.rect.x, self.rect.y = self.pos.x, self.pos.y

    def hit(self, damage):
        self.hp -= damage

    def check(self, other_objects_group):
        for tile in other_objects_group:
            if pygame.sprite.collide_mask(self, tile):
                self.collide = tile
                return True
        return False


class ExpOrb(pygame.sprite.Sprite):
    def __init__(self, exp, pos, orbs_group, all_sprites):
        super().__init__(orbs_group, all_sprites)
        self.exp = exp
        self.image = pygame.Surface((5, 5))
        self.image.fill('white')
        self.rect = self.image.get_rect().move(*pos)

    def apply_changes(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
