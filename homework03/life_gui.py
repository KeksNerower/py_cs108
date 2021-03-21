import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)

        self.cell_size = cell_size
        self.speed = speed
        self.rows = self.life.rows
        self.cols = self.life.cols

        self.height = self.rows * self.cell_size
        self.width = self.cols * self.cell_size

        # Создание нового окна
        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (x, 0), (x, self.height)
            )
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (0, y), (self.width, y)
            )

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i in range(self.rows):
            for j in range(self.cols):

                if self.life.curr_generation[i][j] == 1:
                    color = pygame.Color("green")
                else:
                    color = pygame.Color("white")

                rect = pygame.Rect(
                    j * self.cell_size,
                    i * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )

                pygame.draw.rect(self.screen, color, rect)

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        is_paused = False

        while running:
            # Обработка внешних событий
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        is_paused = not is_paused
                if event.type == pygame.MOUSEBUTTONUP:
                    j, i = pygame.mouse.get_pos()
                    i = i // self.cell_size
                    j = j // self.cell_size
                    self.life.curr_generation[i][j] = int(
                        not bool(self.life.curr_generation[i][j])
                    )

            if not is_paused:
                # Выполнение одного шага игры
                self.life.step()

            # Отрисовка списка клеток
            self.draw_grid()
            self.draw_lines()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    gui = GUI(GameOfLife((20, 30), False), cell_size=15)
    gui.run()
