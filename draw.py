import pygame
from settings import *

class Drawing:
    def __init__(self, sc, sc_map):
        self.sc = sc
        self.sc_map = sc_map
        self.font = pygame.font.SysFont('Arial', 36, bold=True)

    def background(self):
        pygame.draw.rect(self.sc, BLACK, (0, 0, WIDTH, WIDTH // 2))
        pygame.draw.rect(self.sc, DARKGRAY, (0, HEIGHT // 2, WIDTH, HEIGHT // 2))

    def world(self, player, world_map):
        player.ray_casting(self.sc, world_map)  # Вызов метода ray_casting через объект Player

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, WHITE)
        self.sc.blit(render, (WIDTH - 65, 5))

    def mini_map(self, player, mini_map):
        self.sc_map.fill(BLACK)
        map_x, map_y = player.x // 5, player.y // 5
        pygame.draw.line(self.sc_map, LIME, (map_x, map_y), (map_x + 12 * math.cos(player.angle),
                                                 map_y + 12 * math.sin(player.angle)), 2)
        pygame.draw.circle(self.sc_map, LIME, (int(map_x), int(map_y)), 5)
        for x, y in mini_map:
            pygame.draw.rect(self.sc_map, WHITE, (x, y, 20, 20))
        self.sc.blit(self.sc_map, (0, HEIGHT - HEIGHT // 5))