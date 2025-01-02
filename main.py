import pygame.draw
from map import *
from player import *
from view import *

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    sc = pygame.display.set_mode((WIDTH, HEIGHT))
    Player_obj = Player()
    Map = WorldMap()
    Map.create_map() # создание карты
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            # обработка клавиш передвижения
            if event.type == pygame.KEYDOWN and event.key in MOVE_BUTTONS_PRESS.keys():
                MOVE_BUTTONS_PRESS[event.key] = True
            if event.type == pygame.KEYUP and event.key in MOVE_BUTTONS_PRESS.keys():
                MOVE_BUTTONS_PRESS[event.key] = False

        Player_obj.move()

        # отрисовка
        sc.fill(BLACK)
        pygame.draw.line(sc, (0, 255, 0), Player_obj.pos(),
                         (Player_obj.x + WIDTH * math.cos(Player_obj.view),
                          Player_obj.y + HEIGHT * math.sin(Player_obj.view)), 3)  # направление взгляда
        view(sc, Player_obj.pos(), Player_obj.view)  # лучи с обзором
        pygame.draw.circle(sc, (0, 255, 0), Player_obj.pos(), 10)  # игрок
        Map.draw_map(sc)
        pygame.display.flip()
        clock.tick(FPS)
