import pygame
import math
from settings import *
from map import world_map

def ray_casting(sc, player_pos, player_angle, textures):
    ox, oy = player_pos
    mapping = lambda a, b: ((a // WALL_SIZE) * WALL_SIZE, (b // WALL_SIZE) * WALL_SIZE)
    xm, ym = mapping(ox, oy)
    cur_angle = player_angle - FOV / 2
    ray_width = WIDTH // RAYS_INT  # Ширина одного луча на экране

    for ray in range(RAYS_INT):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
        sin_a = sin_a if sin_a else 0.000001
        cos_a = cos_a if cos_a else 0.000001

        # вертикальный перебор
        x, dx = (xm + WALL_SIZE, 1) if cos_a >= 0 else (xm, -1)
        depth_v = float('inf')  # Инициализируем глубину для вертикальных лучей
        texture_v = None  # Инициализируем текстуру для вертикальных лучей
        for i in range(0, WIDTH * 2, WALL_SIZE):  # Увеличиваем диапазон для поиска стен
            depth_v_temp = (x - ox) / cos_a
            yv = oy + depth_v_temp * sin_a
            tile_v = mapping(x + dx, yv)
            if tile_v in world_map:
                depth_v = depth_v_temp
                texture_v = world_map[tile_v]
                break
            x += dx * WALL_SIZE

        # горизонтальный перебор
        y, dy = (ym + WALL_SIZE, 1) if sin_a >= 0 else (ym, -1)
        depth_h = float('inf')
        texture_h = None
        for i in range(0, HEIGHT * 2, WALL_SIZE):
            depth_h_temp = (y - oy) / sin_a
            xh = ox + depth_h_temp * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in world_map:
                depth_h = depth_h_temp
                texture_h = world_map[tile_h]
                break
            y += dy * WALL_SIZE

        if depth_v < depth_h:
            depth, offset, texture = depth_v, yv, texture_v
        else:
            depth, offset, texture = depth_h, xh, texture_h
        if texture is None:
            continue

        offset = int(offset) % WALL_SIZE  # Смещение текстуры в пределах стены
        depth *= math.cos(player_angle - cur_angle)  # Коррекция перспективы
        depth = max(depth, 0.00001)
        proj_height = min(int(PROJ_COEF / depth), 2 * HEIGHT)  # Высота проекции стены

        wall_column = textures[texture].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
        wall_column = pygame.transform.scale(wall_column, (ray_width, proj_height))  # Масштабируем текстуру
        sc.blit(wall_column, (ray * ray_width, HEIGHT // 2 - proj_height // 2))  # Рисуем текстуру

        cur_angle += DELTA_ANGLE