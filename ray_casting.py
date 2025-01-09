import pygame
import math
from settings import *
from map import world_map
from sprites import Sprites  # Импортируем класс спрайтов

def ray_casting(sc, player_pos, player_angle, textures):
    ox, oy = player_pos
    mapping = lambda a, b: ((a // WALL_SIZE) * WALL_SIZE, (b // WALL_SIZE) * WALL_SIZE)
    xm, ym = mapping(ox, oy)
    cur_angle = player_angle - FOV / 2
    ray_width = WIDTH / RAYS_INT

    rays = []  # Список для хранения информации о лучах (глубина, текстура и т.д.)
    sprites = Sprites()  # Создаем объект спрайтов

    for ray in range(RAYS_INT):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)

        # Вертикальное пересечение луча
        x, dx = (xm + WALL_SIZE, 1) if cos_a >= 0 else (xm, -1)
        depth_v = float('inf')
        texture_v = '1'
        for i in range(0, WIDTH * 2, WALL_SIZE):
            depth_v_temp = (x - ox) / cos_a
            yv = oy + depth_v_temp * sin_a
            tile_v = mapping(x + dx, yv)
            if tile_v in world_map:
                depth_v = depth_v_temp
                texture_v = world_map[tile_v]
                break
            x += dx * WALL_SIZE

        # Горизонтальное пересечение луча
        y, dy = (ym + WALL_SIZE, 1) if sin_a >= 0 else (ym, -1)
        depth_h = float('inf')
        texture_h = '1'
        for i in range(0, HEIGHT * 2, WALL_SIZE):
            depth_h_temp = (y - oy) / sin_a
            xh = ox + depth_h_temp * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in world_map:
                depth_h = depth_h_temp
                texture_h = world_map[tile_h]
                break
            y += dy * WALL_SIZE

        # Выбор ближайшего пересечения (вертикального или горизонтального)
        if depth_v < depth_h:
            depth, offset, texture = depth_v, yv, texture_v
        else:
            depth, offset, texture = depth_h, xh, texture_h

        offset = int(offset) % WALL_SIZE
        depth *= math.cos(player_angle - cur_angle)  # Коррекция перспективы
        proj_height = min(int(PROJ_COEF / depth), 2 * HEIGHT)

        rays.append((depth, offset, texture, proj_height))  # Сохраняем информацию о луче
        cur_angle += DELTA_ANGLE

    # Отрисовка стен
    left = 0
    for ray in range(RAYS_INT):
        right = left + ray_width
        left_int = int(left)
        right_int = int(right)
        column_width = right_int - left_int

        if column_width <= 0:
            left = right
            continue

        depth, offset, texture, proj_height = rays[ray]

        # Получаем текстуру и её размеры
        texture_surface = textures[texture]
        texture_width, texture_height = texture_surface.get_size()

        # Рассчитываем offset_px с учетом реального размера текстуры
        offset_px = int(offset * TEXTURE_SCALE)
        offset_px = offset_px % texture_width  # Нормализуем offset

        # Проверка, чтобы offset_px и TEXTURE_SCALE не выходили за пределы текстуры
        if offset_px < 0 or offset_px + TEXTURE_SCALE > texture_width:
            continue  # Пропускаем этот луч, если offset выходит за пределы

        try:
            # Создаем subsurface и масштабируем его
            wall_column = texture_surface.subsurface(offset_px, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
            wall_column = pygame.transform.scale(wall_column, (column_width, proj_height))
            sc.blit(wall_column, (left_int, HEIGHT // 2 - proj_height // 2))
        except ValueError as e:
            continue  # Пропускаем этот луч, если возникает ошибка

        left = right

    # Отрисовка спрайтов
    for sprite in sprites.list_of_objects:
        sprite_x, sprite_y = sprite.pos
        dx, dy = sprite_x - ox, sprite_y - oy
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        # Угол между направлением игрока и спрайтом
        sprite_angle = math.atan2(dy, dx) - player_angle
        if sprite_angle > math.pi:
            sprite_angle -= 2 * math.pi
        elif sprite_angle < -math.pi:
            sprite_angle += 2 * math.pi

        # Проверка, находится ли спрайт в поле зрения
        if -FOV / 2 < sprite_angle < FOV / 2:
            # Позиция спрайта на экране
            sprite_screen_x = int((sprite_angle + FOV / 2) * (WIDTH / FOV))
            sprite_height = int(PROJ_COEF / distance_to_sprite)
            sprite_width = sprite_height

            # Проверка глубины спрайта относительно стен
            ray_index = int(sprite_screen_x / ray_width)
            if ray_index < 0 or ray_index >= len(rays):
                continue  # Пропускаем, если индекс выходит за пределы

            ray_depth = rays[ray_index][0]  # Глубина стены для этого луча

            # Если спрайт ближе, чем стена, отрисовываем его
            if distance_to_sprite < ray_depth:
                # Масштабирование спрайта
                sprite_image = pygame.transform.scale(sprite.object[0], (sprite_width, sprite_height))
                sprite_rect = sprite_image.get_rect()
                sprite_rect.centerx = sprite_screen_x
                sprite_rect.centery = HEIGHT // 2

                # Отрисовка спрайта
                sc.blit(sprite_image, sprite_rect)