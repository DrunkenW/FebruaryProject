import pygame
from settings import *
from player import Player
import math
from map import Map
from draw import Drawing

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
sc_map = pygame.Surface((WIDTH // 5, HEIGHT // 5))
clock = pygame.time.Clock()
Player_obj = Player()
drawing = Drawing(sc, sc_map)
WorldMap = Map()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    Player_obj.movement(WorldMap.get_map())
    sc.fill(BLACK)

    drawing.background()
    drawing.world(Player_obj.pos, Player_obj.angle, WorldMap.get_map())
    drawing.fps(clock)
    drawing.mini_map(Player_obj, WorldMap.get_minimap())

    pygame.display.flip()
    clock.tick(MAX_FPS)