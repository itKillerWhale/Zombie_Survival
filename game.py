import os
import random
import time
import sqlite3

import pygame
from pygame.locals import *
from datetime import datetime
import math

from player.level_system import Level, AbilityChoose, ABILITIES
from player.player import Player
from player.camera import Camera
from player.bullet import Bullet
from enemy.enemy import Enemy
from world.world import Tile
from functions import terminate, load_image

pygame.init()
pygame.display.set_caption("Survive The Apocalypse")
size = width, height = 1280, 720
flags = DOUBLEBUF
FPS = 30
screen = pygame.display.set_mode(size, flags, 16)

PATH = 'resourses/sprites/zombie/'
ZOMBIE_WALK = [pygame.transform.scale(pygame.image.load(image), (51, 65)).convert_alpha() for image in
               [PATH + 'Zombie_Walk1.png', PATH + 'Zombie_Walk2.png', PATH + 'Zombie_Walk3.png',
                PATH + 'Zombie_Walk4.png', PATH + 'Zombie_Walk5.png', PATH + 'Zombie_Walk6.png',
                PATH + 'Zombie_Walk7.png', PATH + 'Zombie_Walk8.png']]

ZOMBIE_WALK_REVERSE = [pygame.transform.flip(image, flip_y=False, flip_x=True).convert_alpha() for image in ZOMBIE_WALK]
SAND_IMAGE = pygame.image.load('resourses/sprites/world/sand.jpg').convert_alpha()
BULLET_IMAGE = pygame.transform.scale(load_image('resourses/sprites/player/bullet.png', -1), (30, 15))
PATH = 'resourses/sprites/world/'
OTHER_OBJECTS_IMAGE = [pygame.transform.scale(pygame.image.load(image), (60, 60)) for image in
                       [PATH + file for file in os.listdir('resourses/sprites/world')]]


def results_screen():
    results = [('Дата и время', 'Достигнутый уровень', 'Количество убийств')]
    database = sqlite3.connect('game_results.db')
    cursor = database.cursor()
    results += cursor.execute('SELECT * FROM results').fetchall()
    database.close()
    fon = pygame.transform.scale(pygame.image.load('resourses/sprites/start_screen/start_screen_fon.jpg'),
                                 (screen.get_width(), screen.get_height()))
    screen.blit(fon, (0, 0))
    pygame.draw.rect(screen, 'white', (50, 50, screen.get_width() - 100, screen.get_height() - 100), border_radius=30)
    for i in range(1, 3):
        pygame.draw.line(screen, 'black', (i * 420, 70), (i * 420, screen.get_height() - 70), width=5)
    for i in range(1, 13):
        pygame.draw.line(screen, 'black', (70, 70 + 45 * i), (screen.get_width() - 70, 70 + 45 * i), width=5)
    for row, elem in enumerate(results[:11]):
        if row == 0:
            font = pygame.font.SysFont('Comic Sans MS', 30)
        else:
            font = pygame.font.SysFont('Comic Sans MS', 25)
        alive_time = font.render(elem[0], True, 'black')
        alive_time_rect = alive_time.get_rect(center=(245, 90 + row * 45))
        screen.blit(alive_time, alive_time_rect)

        level = font.render(elem[1], True, 'black')
        level_rect = level.get_rect(center=(625, 90 + row * 45))
        screen.blit(level, level_rect)

        kills = font.render(elem[2], True, 'black')
        kills_rect = kills.get_rect(center=(1005, 90 + row * 45))
        screen.blit(kills, kills_rect)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    start_screen()


def start_screen():
    font = pygame.font.SysFont('Comic Sans MS', 30)
    start_screen_fon = pygame.transform.scale(pygame.image.load('resourses/sprites/start_screen/start_screen_fon.jpg'),
                                              (screen.get_width(), screen.get_height()))
    screen.blit(start_screen_fon, (0, 0))

    start_game_btn_rect = pygame.Rect(470, 320, 380, 50)
    start_game_btn = font.render('Играть', True, 'black')
    pygame.draw.rect(screen, 'white', start_game_btn_rect, border_radius=20)
    screen.blit(start_game_btn, start_game_btn.get_rect(center=(660, 345)))

    results_btn_rect = pygame.Rect(470, 380, 380, 50)
    results_btn = font.render('Результаты', True, 'black')
    pygame.draw.rect(screen, 'white', results_btn_rect, border_radius=20)
    screen.blit(results_btn, results_btn.get_rect(center=(660, 405)))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(event.pos[0], event.pos[1], 1, 1) in start_game_btn_rect:
                    game()
                if pygame.Rect(event.pos[0], event.pos[1], 1, 1) in results_btn_rect:
                    results_screen()
        pygame.display.flip()
        clock.tick(30)


def end_game_screen(all_sprites, player, level):
    all_sprites.draw(screen)
    player.update_hp_bar(screen)
    level.update(screen)
    font = pygame.font.SysFont('Comic Sans MS', 20)

    pygame.draw.rect(screen, '#1e3130', (390, 235, 500, 250), border_radius=20)

    restart_btn_rect = pygame.Rect(420, 420, 200, 30)
    pygame.draw.rect(screen, 'white', restart_btn_rect, border_radius=10)
    restart = font.render('Играть заново', True, 'black')
    screen.blit(restart, restart.get_rect(center=(520, 433)))

    exit_btn_rect = pygame.Rect(660, 420, 200, 30)
    pygame.draw.rect(screen, 'white', exit_btn_rect, border_radius=10)
    exit = font.render('Выйти в меню', True, 'black')
    screen.blit(exit, exit.get_rect(center=(760, 433)))

    font = pygame.font.SysFont('Comic Sans MS', 20)

    kills_count = font.render(f'Количество убийств: {player.kills}', True, 'white')
    screen.blit(kills_count, (420, 263))

    max_level = font.render(
        f'Достигнутый уровень: {level.level}', True,
        'white')
    screen.blit(max_level, (420, 313))
    max_level_exp = font.render(
        f'({level.level_progress[0]} из {level.level_progress[1]} опыта)', True, 'white')
    screen.blit(max_level_exp, (420, 333))

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(event.pos[0], event.pos[1], 1, 1) in restart_btn_rect:
                    game()
                if pygame.Rect(event.pos[0], event.pos[1], 1, 1) in exit_btn_rect:
                    start_screen()


def pause_screen(player, level):
    pygame.draw.rect(screen, '#1e3130', (490, 235, 300, 250), border_radius=20)
    font = pygame.font.SysFont('Comic Sans MS', 20)

    continue_btn_rect = pygame.Rect(540, 285, 200, 40)
    pygame.draw.rect(screen, 'white', continue_btn_rect, border_radius=10)
    continue_btn = font.render('Продолжить', True, 'black')
    screen.blit(continue_btn, continue_btn.get_rect(center=(640, 300)))

    restart_btn_rect = pygame.Rect(540, 345, 200, 40)
    pygame.draw.rect(screen, 'white', restart_btn_rect, border_radius=10)
    restart_btn = font.render('Играть заново', True, 'black')
    screen.blit(restart_btn, restart_btn.get_rect(center=(640, 360)))

    exit_btn_rect = pygame.Rect(540, 405, 200, 40)
    pygame.draw.rect(screen, 'white', exit_btn_rect, border_radius=10)
    exit_btn = font.render('Выйти в меню', True, 'black')
    screen.blit(exit_btn, exit_btn.get_rect(center=(640, 420)))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    time.sleep(0.15)
                    return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(event.pos[0], event.pos[1], 1, 1) in continue_btn_rect:
                    time.sleep(0.15)
                    return
                if pygame.Rect(event.pos[0], event.pos[1], 1, 1) in restart_btn_rect:
                    out = (
                        str(datetime.today()), f'{level.level} ({level.level_progress[0]}/{level.level_progress[1]})',
                        str(player.kills))
                    insert_data_in_database('game_results.db', out)
                    game()
                if pygame.Rect(event.pos[0], event.pos[1], 1, 1) in exit_btn_rect:
                    out = (
                        str(datetime.today()), f'{level.level} ({level.level_progress[0]}/{level.level_progress[1]})',
                        str(player.kills))
                    insert_data_in_database('game_results.db', out)
                    start_screen()


def insert_data_in_database(database_name, data):
    database = sqlite3.connect(database_name)
    cursor = database.cursor()
    cursor.execute('INSERT INTO Results values (?,?,?)', data)
    database.commit()
    database.close()


def game():
    frames = 0
    last_shot = 0
    game_difficult = 3

    choose_ability = False
    running = True

    tiles_group = pygame.sprite.Group()
    other_objects_group = pygame.sprite.Group()
    orbs_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    player = Player(screen, 10, 5, 30, 30, player_group, all_sprites)
    level = Level(4, 1.3)
    camera = Camera(width, height)
    for y in range(-240, 641, 80):
        for x in range(-240, 1201, 80):
            Tile(x, y, SAND_IMAGE, tiles_group, all_sprites)

    move = (False, False, False, False)

    while running:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                terminate()
            if not choose_ability:
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        pause_screen(player, level)
                        continue
                    move = (keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_w], keys[pygame.K_s])
                if event.type == pygame.KEYUP:
                    move = (keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_w], keys[pygame.K_s])
        if not choose_ability:
            mouse_btn = pygame.mouse.get_pressed()[0]
            screen.fill((0, 0, 0))
            if player.hp[0] <= 0:
                out = (str(datetime.today()), f'{level.level} ({level.level_progress[0]}/{level.level_progress[1]})',
                       str(player.kills))
                insert_data_in_database('game_results.db', out)
                end_game_screen(all_sprites, player, level)
            if pygame.mouse.get_pressed()[0] and frames - last_shot >= player.fire_rate / player.shot_speed:
                if player.magazin[0] > 0:
                    Bullet(bullets_group, player, pygame.mouse.get_pos(), BULLET_IMAGE)
                    player.magazin[0] -= 1
                    last_shot = frames
                    pygame.mixer.Sound("resourses/sounds/shoot.mp3").play()
            if pygame.sprite.spritecollideany(player_group.sprites()[0], orbs_group):
                for orb in pygame.sprite.spritecollide(player_group.sprites()[0], orbs_group, False):
                    level.add_exp(orb.exp)
                    if level.level_up:
                        level.level_up = False
                        choose_ability = True
                        choose_screen = AbilityChoose(player)
                        pygame.mixer.Sound("resourses/sounds/raising_the_level.mp3").play()
                    else:
                        pygame.mixer.Sound("resourses/sounds/gaining_experience_sound.mp3").play()
                    show = 0
                    orb.kill()
            if frames % 120 == 0:
                for _ in range(round(game_difficult)):
                    if len(enemy_group) >= 60:
                        enemy_group.remove(enemy_group.sprites()[0])
                    angle = math.radians(random.randint(0, 360))
                    x, y = math.cos(angle) * 880 + player.rect.x, math.sin(angle) * 600 + player.rect.y
                    Enemy(10, x, y, ZOMBIE_WALK[0], enemy_group, all_sprites)

            left, right, up, down = move
            player_group.update(screen, left, right, up, down, enemy_group, other_objects_group)
            enemy_group.update(player, game_difficult, ZOMBIE_WALK[(frames // 2) % 8],
                               ZOMBIE_WALK_REVERSE[(frames // 2) % 8],
                               orbs_group, enemy_group, other_objects_group, all_sprites)
            bullets_group.update(enemy_group, other_objects_group)

            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)

            tiles_group.update(player.rect, OTHER_OBJECTS_IMAGE, other_objects_group)
            other_objects_group.update(player, other_objects_group, all_sprites)

            tiles_group.draw(screen)
            other_objects_group.draw(screen)
            orbs_group.draw(screen)
            bullets_group.draw(screen)
            player_group.draw(screen)
            enemy_group.draw(screen)
            level.update(screen)
            player.update_hp_bar(screen)

            frames += 1
            game_difficult += 1 / 2000
            # print(clock.get_fps())
            pygame.display.flip()
            clock.tick(FPS)
        else:
            choose = False
            choose_screen.update(screen)
            choose_screen.show_ability(screen, choose_screen.btns[show][0], show)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i in range(3):
                        if not choose:
                            if pygame.Rect(event.pos[0], event.pos[1], 1, 1) in choose_screen.btns[i][1]:
                                show = i
                            if pygame.Rect(event.pos[0], event.pos[1], 1, 1) in choose_screen.accept_btn_rect:
                                exec(choose_screen.btns[show][0][1])
                                if choose_screen.btns[show][0][0] in [elem for elem in ABILITIES.keys()]:
                                    player.had.append(choose_screen.btns[show][0][0])
                                choose = True
                                choose_ability = False
                                move = (False, False, False, False)
                                time.sleep(0.15)
                pygame.display.flip()


if __name__ == '__main__':
    screen.fill(pygame.Color("black"))
    pygame.display.flip()
    screen.set_alpha(None)
    clock = pygame.time.Clock()
    start_screen()
    game()

    terminate()
