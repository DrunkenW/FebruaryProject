import pygame
from settings import *

class Weapon:
    def __init__(self, name, damage, cooldown, fire_animation, reload_animation, idle_animation,
                 fire_sound, max_ammo=6):
        self.fire_sound = fire_sound
        self.name = name
        self.damage = damage
        self.cooldown = cooldown
        self.last_shot = 0
        self.fire_animation = fire_animation
        self.reload_animation = reload_animation
        self.idle_animation = idle_animation  # Нейтральный кадр
        self.current_frame = 0
        self.is_firing = False
        self.is_reloading = False
        self.animation_speed = 100
        self.last_frame_time = 0
        self.max_ammo = max_ammo
        self.ammo = max_ammo


    def can_shoot(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.last_shot >= self.cooldown

    def shoot(self):
        if self.can_shoot() and self.ammo > 0:
            self.ammo -= 1  # Уменьшаем патроны при выстреле
            self.fire_sound.play()
            self.last_shot = pygame.time.get_ticks()
            self.is_firing = True
            self.current_frame = 0
            return True
        return False

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_time > self.animation_speed:
            self.last_frame_time = current_time
            if self.is_firing:
                self.current_frame += 1
                if self.current_frame >= len(self.fire_animation):
                    self.is_firing = False
                    self.current_frame = 0

    def get_current_frame(self):
        if self.is_firing:
            return self.fire_animation[self.current_frame]
        elif self.is_reloading:
            return self.reload_animation[self.current_frame]
        else:
            return self.idle_animation[0]  # Возвращаем нейтральный кадр