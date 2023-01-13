import random
import time

import pygame
from pygame.locals import *
import math

from player.abilties import AbilityChoose
from player.level_system import Level
from player.player import Player
from player.camera import Camera
from player.bullet import Bullet
from enemy.enemy import Enemy, ExpOrb
from world.world import Tile
from functions import terminate

pygame.init()
pygame.display.set_caption("project")
size = width, height = 1280, 720
flags = DOUBLEBUF
screen = pygame.display.set_mode(size, flags, 16)

PATH = 'resourses/sprites/zombie/'
ZOMBIE_WALK = [pygame.image.load(image).convert_alpha() for image in
               [PATH + 'Zombie_Walk1.png', PATH + 'Zombie_Walk2.png', PATH + 'Zombie_Walk3.png',
                PATH + 'Zombie_Walk4.png', PATH + 'Zombie_Walk5.png', PATH + 'Zombie_Walk6.png',
                PATH + 'Zombie_Walk7.png', PATH + 'Zombie_Walk8.png', PATH + 'Zombie_Walk9.png',
                PATH + 'Zombie_Walk10.png']]

ZOMBIE_WALK_REVERSE = [pygame.transform.flip(image, flip_y=False, flip_x=True) for image in ZOMBIE_WALK]
SAND_IMAGE = pygame.image.load('resourses/sprites/world/sand.jpg').convert_alpha()

if __name__ == '__main__':
    running = True
    fps = 30
    screen.fill(pygame.Color("black"))
    pygame.display.flip()
    screen.set_alpha(None)
    clock = pygame.time.Clock()

    frames = 0
    last_shot = 0
    game_difficult = 2

    choose_ability = False

    tiles_group = pygame.sprite.Group()
    orbs_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    player = Player(screen, 100, 30, 30, player_group, all_sprites)
    level = Level(5, 1.5)
    camera = Camera(width, height)
    for y in range(-240, 641, 80):
        for x in range(-240, 1201, 80):
            Tile(x, y, SAND_IMAGE, tiles_group, all_sprites)

    move = (False, False, False, False)

    while running:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            if not choose_ability:
                if event.type == pygame.KEYDOWN:
                    move = (keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_w], keys[pygame.K_s])
                if event.type == pygame.KEYUP:
                    move = (keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_w], keys[pygame.K_s])
        if not choose_ability:
            screen.fill((0, 0, 0))
            if pygame.mouse.get_pressed()[0] and frames - last_shot >= 900 / player.shot_speed:
                Bullet(bullets_group, player.rect, pygame.mouse.get_pos())
                last_shot = frames
                pygame.mixer.Sound("resourses/sounds/shoot.mp3").play()
            if pygame.sprite.spritecollideany(player_group.sprites()[0], orbs_group):
                for orb in pygame.sprite.spritecollide(player_group.sprites()[0], orbs_group, False):
                    result = level.add_exp(orb.exp)
                    if result:
                        choose_ability = True
                    orb.kill()
            if frames % 60 == 0:
                for _ in range(round(game_difficult)):
                    angle = math.radians(random.randint(0, 360))
                    x, y = math.cos(angle) * 880 + player.rect.x, math.sin(angle) * 600 + player.rect.y
                    Enemy(10, x, y, ZOMBIE_WALK[0], enemy_group, all_sprites)

            left, right, up, down = move
            player_group.update(screen, left, right, up, down, enemy_group)
            enemy_group.update(player, ZOMBIE_WALK[(frames // 2) % 10], ZOMBIE_WALK_REVERSE[(frames // 2) % 10],
                               orbs_group, enemy_group, all_sprites)
            bullets_group.update(enemy_group)

            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)

            tiles_group.update(player.rect)

            tiles_group.draw(screen)
            orbs_group.draw(screen)
            bullets_group.draw(screen)
            player_group.draw(screen)
            enemy_group.draw(screen)
            level.update(screen)
            player.update_hp_bar(screen)

            frames += 1
            game_difficult += 1 / 1000
            pygame.display.flip()
            clock.tick(fps)
        else:
            choose_screen = AbilityChoose(screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i in range(3):
                        if pygame.Rect(event.pos[0], event.pos[1], 1, 1) in choose_screen.abilities[i][1]:
                            choose_ability = False
                            move = (False, False, False, False)
                            time.sleep(0.1)
                pygame.display.flip()
    terminate()
