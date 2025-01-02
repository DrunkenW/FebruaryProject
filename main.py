from settings import *
from player import *

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    sc = pygame.display.set_mode((WIDTH, HEIGHT))
    Player_obj = Player()
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

        # отрисовка игрока
        sc.fill(BLACK)
        pygame.draw.line(sc, (0, 255, 0), Player_obj.pos(),
                         (Player_obj.x + WIDTH * math.cos(Player_obj.view),
                          Player_obj.y + HEIGHT * math.sin(Player_obj.view)))
        pygame.draw.circle(sc, (0, 255, 0), Player_obj.pos(), 10)

        pygame.display.flip()
        clock.tick(FPS)
