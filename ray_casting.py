import pygame
import math
from settings import *
from map import world_map

def ray_casting(sc, player_pos, player_angle, textures):
    ox, oy = player_pos
    mapping = lambda a, b: ((a // WALL_SIZE) * WALL_SIZE, (b // WALL_SIZE) * WALL_SIZE)  # Округление координат до размера стены
    xm, ym = mapping(ox, oy)  # Округленные координаты игрока
    cur_angle = player_angle - FOV / 2  # Начальный угол для первого луча
    ray_width = WIDTH / RAYS_INT  # Ширина одного луча

    rays = []

    for ray in range(RAYS_INT):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)

        # Вертикальное пересечение луча
        x, dx = (xm + WALL_SIZE, 1) if cos_a >= 0 else (xm, -1)  # Начальная позиция и направление
        depth_v = float('inf')  # начальная глубина
        texture_v = '1'  # Default texture for vertical intersection
        for i in range(0, WIDTH * 2, WALL_SIZE):  # Перебор вертикальных линий
            depth_v_temp = (x - ox) / cos_a  # Временная глубина до пересечения
            yv = oy + depth_v_temp * sin_a  # Координата y пересечения
            tile_v = mapping(x + dx, yv)  # Округленные координаты пересечения
            if tile_v in world_map:  # обработка пересечения со стеной
                depth_v = depth_v_temp
                texture_v = world_map[tile_v]
                break
            x += dx * WALL_SIZE  # Переход к следующей вертикальной линии

        # Горизонтальное пересечение луча
        y, dy = (ym + WALL_SIZE, 1) if sin_a >= 0 else (ym, -1)  # Начальная позиция и направление
        depth_h = float('inf')
        texture_h = '1'  # Default texture for horizontal intersection
        for i in range(0, HEIGHT * 2, WALL_SIZE):
            depth_h_temp = (y - oy) / sin_a  # Временная глубина до пересечения
            xh = ox + depth_h_temp * cos_a  # Координата x пересечения
            tile_h = mapping(xh, y + dy)  # Округленные координаты пересечения
            if tile_h in world_map:
                depth_h = depth_h_temp
                texture_h = world_map[tile_h]
                break
            y += dy * WALL_SIZE  # Переходим к следующей горизонтальной линии

        # Выбор ближайшего пересечения (вертикального или горизонтального)
        if depth_v < depth_h:
            depth, offset, texture = depth_v, yv, texture_v  # Используем вертикальное пересечение
        else:
            depth, offset, texture = depth_h, xh, texture_h  # Используем горизонтальное пересечение

        offset = int(offset) % WALL_SIZE  # Смещение текстуры в пределах стены
        depth *= math.cos(player_angle - cur_angle)  # Коррекция перспективы
        proj_height = min(int(PROJ_COEF / depth), 2 * HEIGHT)  # Высота проекции стены

        rays.append((depth, offset, texture, proj_height))  # Сохраняем информацию о луче
        cur_angle += DELTA_ANGLE  # Переход к следующему лучу

    # Отрисовка колонок на экране
    left = 0  # Начальная позиция для отрисовки
    for ray in range(RAYS_INT):
        right = left + ray_width  # Правая граница текущего луча
        left_int = int(left)  # Целочисленная левая граница
        right_int = int(right)  # Целочисленная правая граница
        column_width = right_int - left_int  # Ширина колонки

        if column_width <= 0:  # Если ширина колонки меньше или равна нулю, пропускаем
            left = right
            continue

        depth, offset, texture, proj_height = rays[ray]
        wall_column = textures[texture].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
        wall_column = pygame.transform.scale(wall_column, (column_width, proj_height))  # Масштабируем текстуру
        sc.blit(wall_column, (left_int, HEIGHT // 2 - proj_height // 2))  # Отрисовываем колонку на экране

        left = right  # Переход к следующей колонке

    # Обработка последней колонки (если осталось место)
    if left < WIDTH:
        last_column_width = int(WIDTH - left)  # Ширина последней колонки
        if last_column_width > 0:
            depth, offset, texture, proj_height = rays[-1]
            wall_column = textures[texture].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
            wall_column = pygame.transform.scale(wall_column, (last_column_width, proj_height))
            sc.blit(wall_column, (int(left), HEIGHT // 2 - proj_height // 2))