import random

import pygame

from player.player import Player
from player.camera import Camera
from player.bullet import Bullet
from enemy.enemy import Enemy
from world.world import Tile
from functions import load_image

pygame.init()
pygame.display.set_caption("project")
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)

if __name__ == '__main__':
    running = True
    fps = 30
    frames = 0
    screen.fill(pygame.Color("black"))
    pygame.display.flip()
    clock = pygame.time.Clock()

    tiles_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    player = Player(30, 30, player_group, all_sprites)
    camera = Camera(width, height)
    enemy = Enemy(50, 400, 400, enemy_group, all_sprites)
    for y in range(-240, 641, 80):
        for x in range(-240, 1201, 80):
            Tile(x, y, tiles_group, all_sprites)
    # title = Tile(-160, 50, tiles_group, all_sprites)

    move = (False, False, False, False)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                Bullet(bullets_group, player.rect, event.pos)
                pygame.mixer.Sound("resourses/sounds/shoot.mp3").play()

            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                move = (keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_w], keys[pygame.K_s])

            if event.type == pygame.KEYUP:
                keys = pygame.key.get_pressed()
                move = (keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_w], keys[pygame.K_s])

        screen.fill((0, 0, 0))
        if frames % 1 == 0:
            x = random.choice([random.randint(-200, 0), random.randint(1280, 1480)])
            y = random.choice([random.randint(-200, 0), random.randint(720, 920)])
            Enemy(10, x, y, enemy_group, all_sprites)

        left, right, up, down = move
        player_group.update(left, right, up, down)
        enemy_group.update(player.rect, enemy_group)
        bullets_group.update(enemy_group)

        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

        tiles_group.update(player.rect)

        tiles_group.draw(screen)
        bullets_group.draw(screen)
        enemy_group.draw(screen)
        player_group.draw(screen)

        frames += 1
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
