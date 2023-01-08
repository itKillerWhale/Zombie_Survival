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

        self.pos = pygame.math.Vector2(x, y)

    def apply_changes(self, dx, dy):
        self.pos.x += dx
        self.pos.y += dy

    def update(self, player_pos, other_sprites):
        delta_vector = pygame.Vector2(player_pos.x, player_pos.y) - self.pos
        vector_len = delta_vector.length()
        if vector_len > 0:
            self.pos += delta_vector / vector_len * min(vector_len, self.speed)

            self.rect.x, self.rect.y = self.pos.x, self.pos.y

        if self.hp <= 0:
            self.kill()

    def hit(self, damage):
        self.hp -= damage
