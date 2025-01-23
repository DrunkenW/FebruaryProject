import pygame
from settings import *
from player import Player
import math
from draw import Drawing
from map import walls
pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
player = Player(walls)  # Pass the walls list to the Player constructor
drawing = Drawing(sc)
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and player.mouse_locked:  # Проверка блокировки
                player.shoot()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                player.mouse_locked = not player.mouse_locked
                pygame.mouse.set_visible(not player.mouse_locked)
                pygame.event.set_grab(player.mouse_locked)
                # При разблокировке верните курсор в центр
                if player.mouse_locked:
                    pygame.mouse.set_pos((WIDTH // 2, HEIGHT // 2))


    player.movement()
    sc.fill(BLACK)

    drawing.background(player.angle)
    drawing.world(player.pos, player.angle)
    drawing.fps(clock)
    drawing.draw_hud(player.health)
    for weapon in player.inventory.values():
        weapon.update_animation()

    drawing.draw_weapon(player.inventory[player.current_weapon].get_current_frame())  # Отрисовка текущего кадра оружия

    pygame.display.flip()
    clock.tick(MAX_FPS)