import pygame
from settings import *
from map import world_map


def mapping(a, b):
    return (a // WALL_SIZE) * WALL_SIZE, (b // WALL_SIZE) * WALL_SIZE


def ray_casting(player, textures):
    walls = []
    ox, oy = player.pos
    xm, ym = mapping(ox, oy)
    cur_angle = player.angle - HALF_FOV
    for ray in range(RAYS_INT):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
        sin_a = sin_a if sin_a else 0.000001
        cos_a = cos_a if cos_a else 0.000001

        # verticals
        x, dx = (xm + WALL_SIZE, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, WIDTH, WALL_SIZE):
            depth_v = (x - ox) / cos_a
            yv = oy + depth_v * sin_a
            tile_v = mapping(x + dx, yv)
            if tile_v in world_map:
                texture_v = world_map[tile_v]
                break
            x += dx * WALL_SIZE

        # horizontals
        y, dy = (ym + WALL_SIZE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, HEIGHT, WALL_SIZE):
            depth_h = (y - oy) / sin_a
            xh = ox + depth_h * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in world_map:
                texture_h = world_map[tile_h]
                break
            y += dy * WALL_SIZE

        # projection
        depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
        offset = int(offset) % WALL_SIZE
        depth *= math.cos(player.angle - cur_angle)
        depth = max(depth, 0.00001)
        proj_height = min(int(PROJ_COEF / depth), 2 * HEIGHT)

        wall_column = textures[texture].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
        wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))
        wall_pos = (ray * SCALE, HEIGHT // 2 - proj_height // 2)

        walls.append((depth, wall_column, wall_pos))
        cur_angle += DELTA_ANGLE
    return walls