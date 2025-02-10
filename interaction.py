"""Этот модуль отвечает за взаимодействие игрока с NPC и объектами на карте.
Включает логику для проверки видимости NPC игроком, перемещения NPC и обработки коллизий.
Также содержит методы для очистки мира от удаленных объектов."""

from settings import *
from map import world_map
from ray_casting import mapping
import math
import pygame
from numba import njit

# Скорость перемещения NPC
NPC_SPEED = 1.5

def ray_casting_npc_player(npc_x, npc_y, world_map, player_pos):
    """
    Проверяет, видит ли NPC игрока, используя алгоритм ray casting.
    Возвращает True, если игрок виден, иначе False.
    """
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    delta_x, delta_y = ox - npc_x, oy - npc_y
    cur_angle = math.atan2(delta_y, delta_x)
    cur_angle += math.pi

    sin_a = math.sin(cur_angle)
    sin_a = sin_a if sin_a else 0.000001
    cos_a = math.cos(cur_angle)
    cos_a = cos_a if cos_a else 0.000001

    # Проверка вертикальных стен
    x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
    max_depth = delta_x if cos_a >= 0 else -delta_x
    for i in range(0, int(max_depth) // TILE):
        depth_v = (x - ox) / cos_a
        yv = oy + depth_v * sin_a
        tile_v = mapping(x + dx, yv)
        if tile_v in world_map:
            return False
        x += dx * TILE

    # Проверка горизонтальных стен
    y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
    max_depth = delta_y if sin_a >= 0 else -delta_y
    for i in range(0, int(max_depth) // TILE):
        depth_h = (y - oy) / sin_a
        xh = ox + depth_h * cos_a
        tile_h = mapping(xh, y + dy)
        if tile_h in world_map:
            return False
        y += dy * TILE
    return True


class Interaction:
    def __init__(self, player, sprites, drawing):
        """
        Инициализация класса взаимодействия.
        player: объект игрока.
        sprites: объект, содержащий список всех спрайтов.
        drawing: объект, отвечающий за отрисовку.
        """
        self.player = player
        self.sprites = sprites
        self.drawing = drawing


    def npc_action(self):
        #Обрабатывает действия NPC, включая проверку видимости игрока и перемещение NPC.

        for obj in self.sprites.list_of_objects:
            if obj.flag == 'npc' and not obj.is_dead:
                if ray_casting_npc_player(obj.x, obj.y,
                                          world_map, self.player.pos):
                    obj.npc_action_trigger = True
                    self.npc_move(obj)
                else:
                    obj.npc_action_trigger = False

    def npc_move(self, obj):
        #Перемещает NPC в направлении игрока, учитывая коллизии с объектами на карте.

        if obj.distance_to_sprite > TILE:
            dx = self.player.pos[0] - obj.x
            dy = self.player.pos[1] - obj.y
            angle = math.atan2(dy, dx)

            # Рассчитываем шаг с учетом размера спрайта
            step_x = math.cos(angle) * NPC_SPEED
            step_y = math.sin(angle) * NPC_SPEED

            # Проверяем коллизии для обеих осей отдельно
            new_x = obj.x + step_x
            new_y = obj.y + step_y

            # Получаем все тайлы вокруг новой позиции
            tiles_to_check = [
                mapping(new_x - 20, new_y - 20),  # Левый верхний угол
                mapping(new_x + 20, new_y - 20),  # Правый верхний
                mapping(new_x - 20, new_y + 20),  # Левый нижний
                mapping(new_x + 20, new_y + 20)  # Правый нижний
            ]

            # Проверяем все углы спрайта
            if not any(tile in world_map for tile in tiles_to_check):
                obj.x = new_x
                obj.y = new_y
            else:
                # Пытаемся двигаться по осям отдельно
                if not any(tile in world_map for tile in [
                    mapping(new_x - 20, obj.y - 20),
                    mapping(new_x + 20, obj.y - 20),
                    mapping(new_x - 20, obj.y + 20),
                    mapping(new_x + 20, obj.y + 20)
                ]):
                    obj.x = new_x

                elif not any(tile in world_map for tile in [
                    mapping(obj.x - 20, new_y - 20),
                    mapping(obj.x + 20, new_y - 20),
                    mapping(obj.x - 20, new_y + 20),
                    mapping(obj.x + 20, new_y + 20)
                ]):
                    obj.y = new_y

    def clear_world(self):

        #Очищает мир от объектов, помеченных на удаление.

        deleted_objects = self.sprites.list_of_objects[:]
        [self.sprites.list_of_objects.remove(obj) for obj in deleted_objects if obj.delete]