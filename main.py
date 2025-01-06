import pygame
from settings import *
from player import Player
import math
from map import world_map
from draw import Drawing

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
sc_map = pygame.Surface((WIDTH // 5, HEIGHT // 5))
clock = pygame.time.Clock()
Player_obj = Player()
drawing = Drawing(sc, sc_map)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    Player_obj.movement()
    sc.fill(BLACK)

    drawing.background()
    drawing.world(Player_obj.pos, Player_obj.angle)
    drawing.fps(clock)
    drawing.mini_map(Player_obj)

    pygame.display.flip()
    clock.tick(MAX_FPS)