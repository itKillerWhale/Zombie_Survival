import pygame


class Level:
    def __init__(self, first_lvl_need, level_muptiplier):
        self.total_exp = 0
        self.level_muptiplier = level_muptiplier
        self.level = 1
        self.level_progress = [0, first_lvl_need]

    def update(self, screen):
        pygame.draw.rect(screen, 'gray', (70, 40, 300, 20), border_radius=10)
        pygame.draw.rect(screen, 'green', (70, 40, 300 * self.level_progress[0] / self.level_progress[1], 20),
                         border_radius=10)

    def add_exp(self, exp):
        self.level_progress[0] += exp
        if self.level_progress[0] >= self.level_progress[1]:
            self.level_progress[0] -= self.level_progress[1]
            self.level += 1
            self.level_progress[1] *= self.level_muptiplier
