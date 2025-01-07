import pygame
from settings import *
from player import Player
from map import Map
from draw import Drawing

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
sc_map = pygame.Surface((WIDTH // 5, HEIGHT // 5))
clock = pygame.time.Clock()
player = Player()  # Создаём объект Player
drawing = Drawing(sc, sc_map)
world_map = Map()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    player.movement(world_map.get_map())  # Обновляем движение игрока
    sc.fill(BLACK)

    drawing.background()
    drawing.world(player, world_map.get_map())  # Передаём объект Player в метод world
    drawing.fps(clock)
    drawing.mini_map(player, world_map.get_minimap())

    pygame.display.flip()
    clock.tick(MAX_FPS)