import pygame


class AbilityChoose:
    def __init__(self, screen):
        pygame.draw.rect(screen, '#1e3130', (390, 235, 500, 250), border_radius=20)
        self.abilities = []
        for i in range(3):
            ability = None
            ability_rect = pygame.Rect(445 + 155 * i, 300, 80, 80)
            pygame.draw.rect(screen, 'white', (445 + 155 * i, 300, 80, 80), border_radius=10)
            self.abilities.append((ability, ability_rect))

