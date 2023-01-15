import random

import pygame

BUFFS = {'Увеличивает урон на 5%': 'player.damage += player.start_damage / 20',
         'Увеличивает урон на 10%': 'player.damage += player.start_damage / 10',
         'Увеличивает урон на 15%': 'player.damage += player.start_damage / (100 / 15)'}

UNCOMMON_ABILITIES = {'С шансом 20% замораживает врага на 2 секунды': 'player.frozen = True, player.cur_frame'}

ABILITIES_CHANCES = [UNCOMMON_ABILITIES]

ALL_ABILITIES = UNCOMMON_ABILITIES


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
        while self.level_progress[0] >= self.level_progress[1]:
            self.level_progress[0] -= self.level_progress[1]
            self.level += 1
            self.level_progress[1] *= self.level_muptiplier
            self.level_progress[1] = round(self.level_progress[1])
        return True


class AbilityChoose:
    def __init__(self, player):
        self.abilities = []
        additional_ability = random.choice(ABILITIES_CHANCES)
        for elem in random.choices(list(BUFFS) + list(additional_ability.keys()), k=3):
            elem2 = elem
            while elem2 in self.abilities or elem2 in player.had:
                additional_ability = random.choice(ABILITIES_CHANCES)
                elem2 = random.choice(list(BUFFS) + list(additional_ability.keys()))
            self.abilities.append(elem2)
        self.accept_btn_rect = pygame.Rect(540, 400, 200, 30)
        self.btns = []

    def update(self, screen):
        self.btns = []
        all_buffs = BUFFS | UNCOMMON_ABILITIES
        pygame.draw.rect(screen, '#1e3130', (390, 235, 500, 250), border_radius=20)
        pygame.draw.rect(screen, 'white', self.accept_btn_rect, border_radius=10)
        font = pygame.font.SysFont('Comic Sans MS', 20)
        accept = font.render('Выбрать', True, 'black')
        screen.blit(accept, accept.get_rect(center=(640, 413)))
        for i in range(3):
            ability = self.abilities[i], all_buffs[self.abilities[i]]
            ability_rect = pygame.Rect(480 + 135 * i, 250, 40, 40)
            font = pygame.font.SysFont('Comic Sans MS', 25)
            number = font.render(f'{i + 1}', True, 'white')
            screen.blit(number, (492 + 135 * i, 252))
            self.btns.append((ability, ability_rect))

    def show_ability(self, screen, ability, show):
        font = pygame.font.SysFont('Comic Sans MS', 20)
        ability_text = font.render(ability[0], True, 'white')
        ability_text_rect = ability_text.get_rect(center=(640, 340))
        pygame.draw.rect(screen, 'white', (480 + 135 * show, 250, 40, 40), border_radius=20, width=2)
        screen.blit(ability_text, ability_text_rect)

# class Poison:
#     def __init__(self, ):
