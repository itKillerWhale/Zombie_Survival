import pygame

from player.player import Player
from player.camera import Camera
from player.bullet import Bullet
from enemy.enemy import Enemy
from world.world import World

from functions import load_image

pygame.init()
pygame.display.set_caption("project")
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)

if __name__ == '__main__':
    running = True
    v = 30
    fps = 60
    screen.fill(pygame.Color("black"))
    pygame.display.flip()
    clock = pygame.time.Clock()

    tiles_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    moving_objects_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    player = Player(50, 50, player_group, all_sprites)
    camera = Camera(width, height)
    enemy = Enemy(1000, 700, enemy_group, all_sprites)
    enemy.move_to_player(player_group.sprites()[0])

    move = (False, False, False, False)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                Bullet(moving_objects_group, player.rect, event.pos)
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                move = (keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_w], keys[pygame.K_s])

            if event.type == pygame.KEYUP:
                keys = pygame.key.get_pressed()
                move = (keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_w], keys[pygame.K_s])

        screen.fill((0, 0, 0))

        enemy_group.sprites()[0].move_to_player(player_group.sprites()[0])

        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

        left, right, up, down = move
        player_group.update(left, right, up, down)
        enemy_group.update()
        moving_objects_group.update()

        all_sprites.draw(screen)
        moving_objects_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(v)
    pygame.quit()
