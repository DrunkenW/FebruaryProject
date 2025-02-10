"""Этот модуль отвечает за управление спрайтами в игре, включая их анимацию, позиционирование и взаимодействие с игроком.
Класс Sprites содержит параметры и список объектов (спрайтов), которые размещаются на карте.
Класс SpriteObject управляет отдельными спрайтами, их анимацией, коллизиями и отображением на экране."""

import pygame
from settings import *
from collections import deque

class Sprites:
    def __init__(self):
        # Параметры для каждого типа спрайта
        self.sprite_parameters = {
            'barrel': {
                'sprite': pygame.image.load('sprites/barrel/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 1.8,
                'scale': (0.4, 0.4),
                'side': 30,
                'animation': deque([pygame.image.load(f'sprites/barrel/anim/{i}.png').convert_alpha() for i in range(12)]),
                'is_dead': None,
                'dead_shift': 2.6,
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': True,
                'flag': 'decor',
                'obj_action': []
            },
            'devil': {
                'sprite': [pygame.image.load(f'sprites/devil/base/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': 0.0,
                'scale': (1.1, 1.1),
                'side': 50,
                'animation': [],
                'is_dead': None,
                'dead_shift': 0.6,
                'animation_dist': None,
                'animation_speed': 10,
                'blocked': True,
                'flag': 'npc',
                'obj_action': deque([pygame.image.load(f'sprites/devil/anim/{i}.png').convert_alpha() for i in range(9)]),
            }
        }
        # Список объектов на карте
        self.list_of_objects = [
            # Монстры (5 шт) - стратегические точки
            SpriteObject(self.sprite_parameters['devil'], (4.5, 3.5)),
            SpriteObject(self.sprite_parameters['devil'], (16.5, 6.5)),
            SpriteObject(self.sprite_parameters['devil'], (10.5, 12.5)),
            SpriteObject(self.sprite_parameters['devil'], (22.5, 9.5)),
            SpriteObject(self.sprite_parameters['devil'], (7.5, 15.5)),
            # Бочки x2 (30 шт) - углы и тупики
            SpriteObject(self.sprite_parameters['barrel'], (2 + 0.9, 3 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (5 + 0.9, 3 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (9 + 0.9, 3 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (14 + 0.9, 3 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (19 + 0.9, 3 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (23 + 0.9, 3 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (4 + 0.9, 5 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (11 + 0.9, 5 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (17 + 0.9, 5 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (21 + 0.9, 5 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (6 + 0.9, 7 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (13 + 0.9, 7 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (18 + 0.9, 7 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (24 + 0.9, 7 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (3 + 0.9, 8 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (8 + 0.9, 8 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (15 + 0.9, 8 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (22 + 0.9, 8 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (5 + 0.9, 10 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (12 + 0.9, 10 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (20 + 0.9, 10 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (7 + 0.9, 11 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (14 + 0.9, 11 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (19 + 0.9, 11 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (2 + 0.9, 13 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (10 + 0.9, 13 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (17 + 0.9, 13 + 0.9)),
            SpriteObject(self.sprite_parameters['barrel'], (23 + 0.9, 13 + 0.9)),
        ]

class SpriteObject:
    def __init__(self, parameters, pos):
        # Инициализация спрайта с заданными параметрами
        self.object = parameters['sprite'].copy()
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation'].copy()
        self.is_dead = parameters['is_dead']
        self.dead_shift = parameters['dead_shift']
        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.blocked = parameters['blocked']
        self.flag = parameters['flag']
        self.obj_action = parameters['obj_action'].copy()
        self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.side = parameters['side']
        self.dead_animation_count = 0
        self.animation_count = 0
        self.npc_action_trigger = False
        self.door_open_trigger = False
        self.door_prev_pos = self.y if self.flag == 'door_h' else self.x
        self.delete = False
        self.distance_to_sprite = 0
        self.collision_rect = pygame.Rect(
            self.x - self.side // 2,
            self.y - self.side // 2,
            self.side,
            self.side
        )
        if self.viewing_angles:
            if len(self.object) == 8:
                self.sprite_angles = [frozenset(range(338, 361)) | frozenset(range(0, 23))] + \
                                     [frozenset(range(i, i + 45)) for i in range(23, 338, 45)]
            else:
                self.sprite_angles = [frozenset(range(348, 361)) | frozenset(range(0, 11))] + \
                                     [frozenset(range(i, i + 23)) for i in range(11, 348, 23)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

    def object_locate(self, player):
        # Определение позиции спрайта относительно игрока
        dx, dy = self.x - player.x, self.y - player.y
        self.distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

    def update_collision_rect(self):
        # Обновление прямоугольника коллизии
        self.collision_rect.center = (self.x, self.y)

    @property
    def is_on_fire(self):
        # Проверка, находится ли спрайт в поле зрения игрока
        if CENTER_RAY - self.side // 2 < self.current_ray < CENTER_RAY + self.side // 2 and self.blocked:
            return self.distance_to_sprite, self.proj_height
        return float('inf'), None

    @property
    def pos(self):
        # Возвращает позицию спрайта
        return self.x - self.side // 2, self.y - self.side // 2

    def object_locate(self, player):
        # Логика определения позиции и отображения спрайта относительно игрока
        dx, dy = self.x - player.x, self.y - player.y
        self.distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        self.theta = math.atan2(dy, dx)
        gamma = self.theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI
        self.theta -= 1.4 * gamma

        delta_rays = int(gamma / DELTA_ANGLE)
        self.current_ray = CENTER_RAY + delta_rays
        if self.flag not in {'door_h', 'door_v'}:
            self.distance_to_sprite *= math.cos(HALF_FOV - self.current_ray * DELTA_ANGLE)

        fake_ray = self.current_ray + FAKE_RAYS
        if 0 <= fake_ray <= FAKE_RAYS_RANGE and self.distance_to_sprite > 30:
            self.proj_height = min(int(PROJ_COEF / self.distance_to_sprite),
                                   HEIGHT * 2)
            sprite_width = int(self.proj_height * self.scale[0])
            sprite_height = int(self.proj_height * self.scale[1])
            half_sprite_width = sprite_width // 2
            half_sprite_height = sprite_height // 2
            shift = half_sprite_height * self.shift

            # Логика для NPC и декораций
            if self.is_dead and self.is_dead != 'immortal':
                sprite_object = self.dead_animation()
                shift = half_sprite_height * self.dead_shift
                sprite_height = int(sprite_height / 1.3)
            elif self.npc_action_trigger:
                sprite_object = self.npc_in_action()
            else:
                self.object = self.visible_sprite()
                sprite_object = self.sprite_animation()

            # Масштабирование и позиционирование спрайта
            sprite_pos = (self.current_ray * SCALE - half_sprite_width, HEIGHT / 2 - half_sprite_height + shift)
            sprite = pygame.transform.scale(sprite_object, (sprite_width, sprite_height))
            return (self.distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)

    def sprite_animation(self):
        # Анимация спрайта
        if self.animation and self.distance_to_sprite < self.animation_dist:
            sprite_object = self.animation[0]
            if self.animation_count < self.animation_speed:
                self.animation_count += 1
            else:
                self.animation.rotate()
                self.animation_count = 0
            return sprite_object
        return self.object

    def visible_sprite(self):
        # Определение видимого спрайта в зависимости от угла обзора
        if self.viewing_angles:
            if self.theta < 0:
                self.theta += DOUBLE_PI
            self.theta = 360 - int(math.degrees(self.theta))

            for angles in self.sprite_angles:
                if self.theta in angles:
                    return self.sprite_positions[angles]
        return self.object

    def npc_in_action(self):
        # Анимация NPC в действии
        sprite_object = self.obj_action[0]
        if self.animation_count < self.animation_speed:
            self.animation_count += 1
        else:
            self.obj_action.rotate()
            self.animation_count = 0
        return sprite_object