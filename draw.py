import pygame
import math
from settings import *
from ray_casting import ray_casting


class Drawing:
    def __init__(self, sc):
        self.sc = sc
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.textures = {
            '1': pygame.image.load('image/wall1.png').convert(),
            '2': pygame.image.load('image/wall2.png').convert(),
            'S': pygame.image.load('image/sky.png').convert()
        }
        self.textures['S'] = pygame.transform.scale(self.textures['S'], (WIDTH, HEIGHT // 2))
        self.hud_image = pygame.image.load('image/hotbar.png').convert_alpha()

        # Scale the HUD image to full screen width
        original_width, original_height = self.hud_image.get_size()
        new_width = WIDTH
        new_height = int((original_height / original_width) * new_width)
        self.hud_image = pygame.transform.scale(self.hud_image, (new_width, new_height))

    def background(self, angle):
        sky_offset = int(-5 * math.degrees(angle)) % WIDTH
        self.sc.blit(self.textures['S'], (sky_offset - WIDTH, 0))
        self.sc.blit(self.textures['S'], (sky_offset, 0))
        self.sc.blit(self.textures['S'], (sky_offset + WIDTH, 0))
        pygame.draw.rect(self.sc, DARKGRAY, (0, HEIGHT // 2, WIDTH, HEIGHT // 2))

    def world(self, player_pos, player_angle):
        ray_casting(self.sc, player_pos, player_angle, self.textures)

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, RED)
        self.sc.blit(render, (WIDTH - 65, 5))

    def draw_hud(self):
        hud_rect = self.hud_image.get_rect()
        hud_rect.bottomleft = (0, HEIGHT)
        self.sc.blit(self.hud_image, hud_rect)