from map import *
from player import Player

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
            if event.type == pygame.KEYDOWN and event.key in BUTTONS_PRESS.keys():
                BUTTONS_PRESS[event.key] = True
            if event.type == pygame.KEYUP and event.key in BUTTONS_PRESS.keys():
                BUTTONS_PRESS[event.key] = False

        # передвижение
        Player_obj.check_press() # проверка зажатия клавиш
        if len([key for key, keydown_bool in BUTTONS_PRESS.items() if keydown_bool]) > 0:
            # выполняется только если есть зажатые клавиши
            Player_obj.move()

        # отрисовка
        sc.fill(BLACK)
        """
        pygame.draw.line(sc, (0, 255, 0), Player_obj.pos(),
                         (Player_obj.x + WIDTH * math.cos(Player_obj.player_direction_of_view),
                          Player_obj.y + HEIGHT * math.sin(Player_obj.player_direction_of_view)), 3)  # направление взгляда

        pygame.draw.circle(sc, (0, 255, 0), Player_obj.pos(), 10)  # игрок

        Map.draw_map(sc) # карта
        """
        Player_obj.vision(sc, Map.get_map())  # лучи с обзором
        pygame.display.flip()
        clock.tick(FPS)
