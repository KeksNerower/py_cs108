import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        rows = self.life.rows
        cols = self.life.cols

        screen.addstr(str("+" + "-" * cols + "+" + "\n"))
        for i in range(rows):
            screen.addstr(str("|" + " " * cols + "|" + "\n"))
        screen.addstr(str("+" + "-" * cols + "+" + "\n"))

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    screen.addch(i + 1, j + 1, "@")

    def run(self) -> None:
        screen = curses.initscr()
        curses.curs_set(0)

        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            screen.clear()

            self.draw_borders(screen)
            self.life.step()
            self.draw_grid(screen)
            screen.refresh()

            curses.napms(200)

        screen.addstr(f"\nIterations: {self.life.generations}\n")
        screen.refresh()
        curses.napms(3000)

        curses.curs_set(1)
        curses.endwin()


if __name__ == "__main__":
    # BE CAREFUL THE FIELD SHOULD NOT BE BIGGER THAN YOUR WINDOW CAN BE MEETED
    console = Console(GameOfLife((20, 20), max_generations=200))
    try:
        console.run()
    except curses.error:
        print("Check the size of the field !")
