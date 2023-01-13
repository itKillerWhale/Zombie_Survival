import math
import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, hp, x, y, image, enemy_group, all_sprites):
        super().__init__(enemy_group, all_sprites)

        self.hp = hp
        self.move_x, self.move_y = 0, 0

        self.speed = 3
        self.cur_frame = 0

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(x, y)

        self.pos = pygame.Vector2(x, y)

    def apply_changes(self, dx, dy):
        self.pos.x += dx
        self.pos.y += dy

    def update(self, player, image, image2, orbs_group, enemy_group, all_sprites):
        player_pos = player.rect
        self.cur_frame += 1
        delta_vector = pygame.Vector2(player_pos.center[0] - 10, player_pos.center[1] + 10) - self.pos
        if math.hypot(player_pos.x - self.rect.x, player_pos.y - self.rect.y) < 900:
            if delta_vector.x > 0:
                self.image = image
            else:
                self.image = image2
        if not (5 <= int(self.cur_frame / 2) % 10 <= 9):
            vector_len = delta_vector.length()
            if vector_len > 0:
                self.pos += delta_vector / vector_len * min(vector_len, self.speed)

        self.rect.x, self.rect.y = self.pos.x, self.pos.y

        if self.hp <= 0:
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

                        self.rect.x, self.rect.y = self.pos.x, self.pos.y

    def hit(self, damage):
        self.hp -= damage


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
