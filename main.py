from settings import *
from player import *
import pygame

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    sc = pygame.display.set_mode((WIDTH, HEIGHT))
    Player_obj = Player()
    FPS = 165
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            # обработка клавиш передвижения
            if event.type == pygame.KEYDOWN and event.unicode.lower() in MOVE_BUTTONS:
                MOVE_BUTTONS_PRESS[event.unicode.lower()] = True
            if event.type == pygame.KEYUP and event.unicode.lower() in MOVE_BUTTONS:
                MOVE_BUTTONS_PRESS[event.unicode.lower()] = False

        Player_obj.move()
        player_pos = (Player_obj.x, Player_obj.y)

        # отрисовка игрока
        sc.fill(BLACK)
        pygame.draw.circle(sc, (0, 255, 0), player_pos, 10)

        pygame.display.flip()
        clock.tick(FPS)
