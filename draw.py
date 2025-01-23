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
        original_width, original_height = self.hud_image.get_size()
        new_width = WIDTH
        self.new_height = int((original_height / original_width) * new_width)
        self.hud_image = pygame.transform.scale(self.hud_image, (new_width, self.new_height))
        self.health_bar_width = 210
        self.health_bar_height = 30
        self.health_bar_x = int(WIDTH * 0.2)

    def draw_weapon(self, weapon_image):
        weapon_x = WIDTH // 2 - weapon_image.get_width() // 2
        weapon_y = HEIGHT - weapon_image.get_height() - 190
        self.sc.blit(weapon_image, (weapon_x, weapon_y))

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

    def draw_hud(self, player_health):
        hud_y = HEIGHT - self.new_height
        self.sc.blit(self.hud_image, (0, hud_y))
        health_bar_y = hud_y + (self.new_height - self.health_bar_height) // 2
        pygame.draw.rect(self.sc, BLACK,
                         (self.health_bar_x, health_bar_y, self.health_bar_width, self.health_bar_height))
        health_width = int((player_health / 100) * self.health_bar_width)
        if health_width < 0:
            health_width = 0
        pygame.draw.rect(self.sc, GREEN,
                         (self.health_bar_x + 2, health_bar_y + 2, health_width, self.health_bar_height - 4))