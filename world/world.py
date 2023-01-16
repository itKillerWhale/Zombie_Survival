import random

import pygame


class Tile(pygame.sprite.Sprite):

    def __init__(self, x, y, image, tiles_group, all_sprites):
        super().__init__(tiles_group, all_sprites)

        self.image = image
        self.all_sprites = all_sprites
        self.rect = self.image.get_rect().move(x, y)

    def apply_changes(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def update(self, player_pos, other_object_image, other_objects_group):
        if player_pos.center[0] - self.rect.x >= 720:
            self.rect.x += 1280 + 80
            self.generate(random.choice(other_object_image), other_objects_group)

        elif player_pos.center[0] - self.rect.x <= -640:
            self.rect.x -= 1280 + 80
            self.generate(random.choice(other_object_image), other_objects_group)

        elif player_pos.center[1] - self.rect.y >= 440:
            self.rect.y += 720 + 80
            self.generate(random.choice(other_object_image), other_objects_group)

        elif player_pos.center[1] - self.rect.y <= -360:
            self.rect.y -= 720 + 80
            self.generate(random.choice(other_object_image), other_objects_group)

    def generate(self, other_object_image, other_objects_group):
        a = random.randint(1, 200)
        if a <= 4:
            OtherObjects(self.rect.x, self.rect.y, other_object_image, other_objects_group, self.all_sprites)


class OtherObjects(pygame.sprite.Sprite):

    def __init__(self, x, y, image, other_objects_group, all_sprites):
        super().__init__(other_objects_group, all_sprites)

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(x, y)

    def update(self, player, other_objects_group, all_sprites):
        for tile in other_objects_group:
            if abs(tile.rect.x - player.rect.x) >= 720 or abs(tile.rect.y - player.rect.y) >= 440:
                other_objects_group.remove(tile)
                all_sprites.remove(tile)

    def apply_changes(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
