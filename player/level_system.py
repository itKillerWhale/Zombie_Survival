import pygame


class Level:
    def __init__(self, first_lvl_need, level_muptiplier):
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.total_exp = 0
        self.level_muptiplier = level_muptiplier
        self.level = 1
        self.level_progress = [0, first_lvl_need]

    def update(self, screen):
        pygame.draw.rect(screen, 'gray', (80, 25, 300, 20), border_radius=10)
        pygame.draw.rect(screen, 'green', (80, 25, 300 * self.level_progress[0] / self.level_progress[1], 20),
                         border_radius=10)
        pygame.draw.circle(screen, 'black', (40, 50), 30)
        text = self.font.render(str(self.level), True, 'white')
        text_rect = text.get_rect(center=(40, 50))
        screen.blit(text, text_rect)

    def add_exp(self, exp):
        self.level_progress[0] += exp
        if self.level_progress[0] >= self.level_progress[1]:
            self.level_progress[0] -= self.level_progress[1]
            self.level += 1
            self.level_progress[1] *= self.level_muptiplier
            return True
