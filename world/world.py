import pygame


class Tile(pygame.sprite.Sprite):

    def __init__(self, x, y, image, tiles_group, all_sprites):
        super().__init__(tiles_group, all_sprites)

        self.image = image
        self.rect = self.image.get_rect().move(x, y)

    def apply_changes(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def update(self, player_pos):
        if player_pos.center[0] - self.rect.x >= 720:
            self.rect.x += 1280 + 80

        elif player_pos.center[0] - self.rect.x <= -640:
            self.rect.x -= 1280 + 80

        elif player_pos.center[1] - self.rect.y >= 440:
            self.rect.y += 720 + 80

        elif player_pos.center[1] - self.rect.y <= -360:
            self.rect.y -= 720 + 80

