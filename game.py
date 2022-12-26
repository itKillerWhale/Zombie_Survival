import pygame

from functions import *
from player.player import Player
from player.camera import Camera

width, height = 1280, 720
running = True
fps = 60
clock = pygame.time.Clock()
left, right, up, down = False, False, False, False
player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Перемещение героя. Камера')
pygame.init()

camera = Camera(width, height)
player = Player(0, 0, player_group, all_sprites)


while running:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left = True
            if event.key == pygame.K_RIGHT:
                right = True
            if event.key == pygame.K_DOWN:
                down = True
            if event.key == pygame.K_UP:
                up = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left = False
            if event.key == pygame.K_RIGHT:
                right = False
            if event.key == pygame.K_DOWN:
                down = False
            if event.key == pygame.K_UP:
                up = False
    screen.fill('black')
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    player_group.update(left, right, up, down)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
