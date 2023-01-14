import random

import pygame

ABILITIES = {'+5% ДМГ': 'player.damage += player.start_damage / 20',
             '+10% ДМГ': 'player.damage += player.start_damage / 10',
             '+15% ДМГ': 'player.damage += player.start_damage / (100 / 15)'}


class Level:
    def __init__(self, first_lvl_need, level_muptiplier):
        pygame.font.init()
        self.total_exp = 0
        self.level_muptiplier = level_muptiplier
        self.level = 1
        self.level_progress = [0, first_lvl_need]

    def update(self, screen):
        pygame.draw.rect(screen, 'gray', (80, 25, 300, 20), border_radius=10)
        pygame.draw.rect(screen, 'green', (80, 25, 300 * self.level_progress[0] / self.level_progress[1], 20),
                         border_radius=10)
        pygame.draw.circle(screen, 'black', (40, 50), 30)

        font = pygame.font.SysFont('Comic Sans MS', 30)
        level = font.render(str(self.level), True, 'white')
        level_rect = level.get_rect(center=(40, 50))

        font = pygame.font.SysFont('Comic Sans MS', 18, bold=True)
        exp = font.render(f'{self.level_progress[0]} / {self.level_progress[1]}', True, 'white')
        exp_rect = level.get_rect(center=(215, 42))

        screen.blit(level, level_rect)
        screen.blit(exp, exp_rect)

    def add_exp(self, exp):
        self.level_progress[0] += exp
        if self.level_progress[0] >= self.level_progress[1]:
            self.level_progress[0] -= self.level_progress[1]
            self.level += 1
            self.level_progress[1] *= self.level_muptiplier
            self.level_progress[1] = round(self.level_progress[1])
            return True


class AbilityChoose:
    def __init__(self):
        self.abilities = random.choices(list(ABILITIES), k=3)
        self.btns = []

    def update(self, screen):
        self.btns = []
        pygame.draw.rect(screen, '#1e3130', (390, 235, 500, 250), border_radius=20)
        for i in range(3):
            ability = self.abilities[i], ABILITIES[self.abilities[i]]
            ability_rect = pygame.Rect(445 + 135 * i, 280, 120, 120)
            self.btns.append((ability, ability_rect))
            font = pygame.font.SysFont('Comic Sans MS', 25)
            ability_text = font.render(ability[0].split()[0], True, 'black')
            ability_text_rect = ability_text.get_rect(center=(505 + 135 * i, 320))
            ability_text2 = font.render(ability[0].split()[1], True, 'black')
            ability_text2_rect = ability_text.get_rect(center=(505 + 135 * i, 340))
            pygame.draw.rect(screen, 'white', (445 + 135 * i, 280, 120, 120), border_radius=10)
            screen.blit(ability_text, ability_text_rect)
            screen.blit(ability_text2, ability_text2_rect)
