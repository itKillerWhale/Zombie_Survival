import pygame

from functions import load_image, cut_sheet


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, hp, damage, x, y, player_group, all_sprites):
        super().__init__(player_group, all_sprites)
        self.player_x, self.player_y = x, y
        self.frames = []
        self.hp = [hp, hp]
        self.damage = damage
        self.speed = 5
        cut_sheet(self, load_image('resourses/sprites/player/player.png', -1), 6, 11)
        self.cur_frame = 0
        self.last_hit = 0
        self.start_damage = self.damage
        self.start_speed = self.speed
        self.percentage = self.hp[0] / self.hp[1]
        self.shot_speed = 90  # Выстрелов в минуту
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale2x(self.image)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(x, y)  # Координаты спавна персонажа

    def apply_changes(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def update_hp_bar(self, screen):
        pygame.draw.rect(screen, 'gray', (80, 50, 240, 20), border_radius=10)
        pygame.draw.rect(screen, 'red', (80, 50, 240 * self.percentage, 20),
                         border_radius=10)
        font = pygame.font.SysFont('Comic Sans MS', 18, bold=True)
        hp = font.render(f'{self.hp[0]} / {self.hp[1]}', True, 'white')
        hp_rect = hp.get_rect(center=(195, 60))

        screen.blit(hp, hp_rect)

    def update(self, screen, left, right, up, down, enemy_group):
        if self.cur_frame - self.last_hit > 30:
            if pygame.sprite.spritecollideany(self, enemy_group):
                self.hp[0] -= 1
                pygame.mixer.Sound("resourses/sounds/damage_sound.mp3").play()
            self.last_hit = self.cur_frame
            try:
                self.percentage = self.hp[0] / self.hp[1]
            except ZeroDivisionError:
                self.percentage = 0
        if left:
            self.rect.x += -self.speed
            self.player_x += -self.speed
        if right:
            self.rect.x += self.speed
            self.player_x += self.speed
        if up:
            self.rect.y += -self.speed
            self.player_y += -self.speed
        if down:
            self.rect.y += self.speed
            self.player_y += self.speed
        self.cur_frame += 1
