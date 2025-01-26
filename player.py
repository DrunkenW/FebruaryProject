from weapon import Weapon
from settings import *

class Player:
    def __init__(self, walls):
        self.x, self.y = start_player_pos
        self.angle = player_angle
        self.speed = player_speed
        self.rotation_speed = TurningSpeed
        self.health = 100
        self.mouse_locked = True  # Флаг блокировки мыши
        pygame.mouse.set_pos((WIDTH // 2, HEIGHT // 2))
        self.inventory = {
            'shotgun': Weapon(
                name='Shotgun',
                damage=50,
                cooldown=1000,
                fire_animation=[pygame.image.load(f'image/shotgun/fire_{i}.png').convert_alpha() for i in range(3)],
                reload_animation=[pygame.image.load(f'image/shotgun/reload_{i}.png').convert_alpha() for i in range(3)],
                idle_animation=[pygame.image.load('image/shotgun/0.png').convert_alpha()],
                max_ammo=6,
                fire_sound=pygame.mixer.Sound(SOUNDS['shotgun'])  # Добавлен звук
            )
        }
        self.current_weapon = 'shotgun'
        self.walls = walls  # Store the walls list

    def switch_weapon(self):
        if self.current_weapon == 'fists':
            self.current_weapon = 'shotgun'
        else:
            self.current_weapon = 'fists'

    def shoot(self):
        weapon = self.inventory[self.current_weapon]
        if weapon.shoot():
            print(f"Shooting with {weapon.name} for {weapon.damage} damage!")
            # Здесь можно добавить логику нанесения урона врагам

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    @property
    def pos(self):
        return self.x, self.y

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()

        # Движение вперед и назад
        if keys[pygame.K_w]:  # Вперед
            new_x = self.x + cos_a * self.speed
            new_y = self.y + sin_a * self.speed
            if not self.check_collision(new_x, new_y):
                self.x, self.y = new_x, new_y
        if keys[pygame.K_s]:  # Назад
            new_x = self.x - cos_a * self.speed
            new_y = self.y - sin_a * self.speed
            if not self.check_collision(new_x, new_y):
                self.x, self.y = new_x, new_y

        # Движение влево и вправо
        if keys[pygame.K_a]:  # Влево
            new_x = self.x + math.cos(self.angle - math.pi / 2) * self.speed
            new_y = self.y + math.sin(self.angle - math.pi / 2) * self.speed
            if not self.check_collision(new_x, new_y):
                self.x, self.y = new_x, new_y
        if keys[pygame.K_d]:  # Вправо
            new_x = self.x + math.cos(self.angle + math.pi / 2) * self.speed
            new_y = self.y + math.sin(self.angle + math.pi / 2) * self.speed
            if not self.check_collision(new_x, new_y):
                self.x, self.y = new_x, new_y

        if self.mouse_locked:
            x, y = pygame.mouse.get_pos()
            center_x, center_y = WIDTH // 2, HEIGHT // 2
            delta_x = x - center_x
            self.angle += delta_x * MOUSE_SENSITIVITY
            pygame.mouse.set_pos((center_x, center_y))
            self.angle %= 2 * math.pi

    def check_collision(self, x, y):
        for wall in self.walls:
            if wall.collidepoint(x, y):
                return True
        return False
