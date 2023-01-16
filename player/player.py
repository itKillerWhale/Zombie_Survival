import pygame

from functions import load_image, cut_sheet


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, hp, damage, x, y, player_group, all_sprites):
        super().__init__(player_group, all_sprites)
        self.screen = screen
        self.player_x, self.player_y = x, y
        self.frames = []
        self.had = []
        self.hp = [hp, hp]
        self.damage = damage
        self.frozen = False, 0
        self.shield = False, 0
        self.vampirizm = False
        self.speed = 5
        self.reload_speed = 90
        self.fire_rate = 900
        self.magazin = [6, 6]
        self.bullet_pierces = 1
        cut_sheet(self, load_image('resourses/sprites/player/player.png', -1), 6, 10)
        self.cur_frame = 0
        self.last_hit = 0
        self.reload = 0, False
        self.kills = 0
        self.start_damage = self.damage
        self.start_speed = self.speed
        self.percentage = self.hp[0] / self.hp[1]
        self.shot_speed = 90  # Выстрелов в минуту
        self.frames = [pygame.transform.scale2x(image) for image in self.frames]
        self.frames_reverse = [pygame.transform.flip(image, True, False) for image in self.frames]
        self.image = self.frames[self.cur_frame]
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

        font = pygame.font.SysFont('Comic Sans MS', 30)
        kills = font.render(f'Убийств: {self.kills}', True, 'white')
        screen.blit(kills, (10, screen.get_height() - 40))

        font = pygame.font.SysFont('Comic Sans MS', 20)
        magazin = font.render(f'Патроны: {self.magazin[0]}/{self.magazin[1]}', True, 'white')
        screen.blit(magazin, (80, 75))

    def update(self, screen, left, right, up, down, enemy_group):
        if right:
            self.image = self.frames[24 + (self.cur_frame // 2) % 6]
        elif left:
            self.image = self.frames_reverse[24 + (self.cur_frame // 2) % 6]
        elif up:
            self.image = self.frames[30 + (self.cur_frame // 2) % 6]
        elif down:
            self.image = self.frames[18 + (self.cur_frame // 2) % 6]
        else:
            self.image = self.frames[(self.cur_frame // 2) % 6]
        if self.magazin[0] <= 0 and not self.reload[1]:
            self.reload = self.cur_frame, True
        if self.reload[1] and self.cur_frame - self.reload[0] > self.reload_speed:
            self.magazin[0] = self.magazin[1]
            self.reload = 0, False
        if self.cur_frame - self.last_hit > 20 and self.cur_frame - self.shield[1] > 90:
            self.last_hit = self.cur_frame
            for enemy in pygame.sprite.spritecollide(self, enemy_group, False):
                if pygame.sprite.collide_mask(self, enemy):
                    if self.shield[0] and self.cur_frame - self.shield[1] > 3600:
                        self.shield = True, self.cur_frame
                        break
                    self.hp[0] -= 1
                    if self.hp[0] == 0:
                        pygame.mixer.Sound("resourses/sounds/game_over.mp3").play()
                    else:
                        pygame.mixer.Sound("resourses/sounds/damage_sound.mp3").play()
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
