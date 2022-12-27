import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_group, all_sprites):
        super().__init__(enemy_group, all_sprites)

        playerx, playery = player_group.sprites[0].rect.x, player_group.sprites[0].rect.y
        delta_x, delta_y = playerx - self.rect.x, playery - self.rect.y
        S = ((self.rect.x - playerx) ** 2 + (self.rect.y - playerx) ** 2) ** (1 / 2)
        self.move_x, self.move_y = delta_x / S, delta_y / S

        self.speedx = 3
        self.speedy = 3

        self.image = pygame.Surface((20, 20))
        self.image.fill('green')
        self.rect = self.image.get_rect().move(x, y)

    def update(self):
        self.rect.x += self.move_x
        self.rect.y += self.move_y

    def move_to_player(self):
        playerx, playery = player_group.sprites[0].rect.x, player_group.sprites[0].rect.y
        delta_x, delta_y = playerx - self.rect.x, playery - self.rect.y
        S = ((self.rect.x - playerx) ** 2 + (self.rect.y - playerx) ** 2) ** (1 / 2)
        self.move_x, self.move_y = delta_x / S, delta_y / S

