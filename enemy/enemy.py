import pygame

from functions import load_image, cut_sheet

PATH = 'resourses/sprites/zombie/'
ZOMBIE_WALK = [pygame.image.load(image) for image in
               [PATH + 'Zombie_Walk1.png', PATH + 'Zombie_Walk2.png', PATH + 'Zombie_Walk3.png',
                PATH + 'Zombie_Walk4.png', PATH + 'Zombie_Walk5.png', PATH + 'Zombie_Walk6.png',
                PATH + 'Zombie_Walk7.png', PATH + 'Zombie_Walk8.png', PATH + 'Zombie_Walk9.png',
                PATH + 'Zombie_Walk10.png']]

ZOMBIE_WALK_REVERSE = [pygame.transform.flip(image, flip_y=False, flip_x=True) for image in ZOMBIE_WALK]


class Enemy(pygame.sprite.Sprite):
    def __init__(self, hp, x, y, enemy_group, all_sprites):
        super().__init__(enemy_group, all_sprites)

        self.hp = hp
        self.move_x, self.move_y = 0, 0

        self.speed = 2

        self.cur_frame = 0
        self.image = ZOMBIE_WALK[self.cur_frame]

        self.rect = self.image.get_rect().move(x, y)

        self.pos = pygame.Vector2(x, y)

    def apply_changes(self, dx, dy):
        self.pos.x += dx
        self.pos.y += dy

    def update(self, player_pos, orbs_group, enemy_group, all_sprites):
        self.cur_frame += 1
        delta_vector = pygame.Vector2(player_pos.center[0] - 10, player_pos.center[1] + 10) - self.pos
        if delta_vector.x > 0:
            self.image = ZOMBIE_WALK[int(self.cur_frame / 2) % 10]
        else:
            self.image = ZOMBIE_WALK_REVERSE[int(self.cur_frame / 2) % 10]
        if not (5 <= int(self.cur_frame / 2) % 10 <= 9):
            vector_len = delta_vector.length()
            if vector_len > 0:
                self.pos += delta_vector / vector_len * min(vector_len, self.speed)

        self.rect.x, self.rect.y = self.pos.x, self.pos.y

        if self.hp <= 0:
            self.kill()
            ExpOrb(1, (self.rect.centerx, self.rect.centery), orbs_group, all_sprites)

        if pygame.sprite.spritecollide(self, enemy_group, False):
            for enemy in pygame.sprite.spritecollide(self, enemy_group, False):
                if enemy != self:
                    enemy_pos = enemy.rect
                    delta_vector = pygame.Vector2(enemy_pos.center[0] - 10,
                                                  enemy_pos.center[1] + 10) - self.pos
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