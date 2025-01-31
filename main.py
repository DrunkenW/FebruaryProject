import pygame
from settings import *
from player import Player
import math
from draw import Drawing
from map import walls
from ray_casting import ray_casting
from sprites import Sprites
from interaction import *
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(SOUNDS['background'])
pygame.mixer.music.play(-1)  # -1 означает бесконечное повторение
pygame.mixer.music.set_volume(0.3)
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
player = Player(walls)
drawing = Drawing(sc)
sprites = Sprites()
interaction = Interaction(player, sprites, drawing)
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and player.mouse_locked:
                player.shoot()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                player.mouse_locked = not player.mouse_locked
                pygame.mouse.set_visible(not player.mouse_locked)
                pygame.event.set_grab(player.mouse_locked)
                if player.mouse_locked:
                    pygame.mouse.set_pos((WIDTH // 2, HEIGHT // 2))

    for obj in sprites.list_of_objects:
        if obj.flag == 'npc':
            obj.update_collision_rect()
    player.movement()
    sc.fill(BLACK)

    interaction.npc_action()
    interaction.clear_world()

    drawing.background(player.angle)
    walls = ray_casting(player, drawing.textures)
    drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])
    drawing.fps(clock)
    drawing.draw_hud(player)
    for weapon in player.inventory.values():
        weapon.update_animation()

    drawing.draw_weapon(player.inventory[player.current_weapon].get_current_frame())

    pygame.display.flip()
    clock.tick(MAX_FPS)