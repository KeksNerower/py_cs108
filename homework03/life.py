import pathlib
import random
import typing as tp
from pprint import pprint as pp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `rows` х `cols`.
        """
        vars = set([0])
        if randomize:
            vars.add(1)

        return [[random.choice(list(vars)) for j in range(self.cols)] for i in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        x, y = cell
        neighbours = []

        for i in range(y - 1, y + 2):
            if i < 0 or i >= self.rows:
                continue

            for j in range(x - 1, x + 2):
                if j < 0 or j >= self.cols:
                    continue

                neighbours.append(self.curr_generation[i][j])
        neighbours.remove(self.curr_generation[y][x])

        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_field = [[*line] for line in self.curr_generation]

        for i in range(self.rows):
            for j in range(self.cols):
                neighbours_amount = self.get_neighbours((j, i)).count(1)

                if neighbours_amount == 3:
                    new_field[i][j] = 1
                elif neighbours_amount != 2:
                    new_field[i][j] = 0

        return new_field

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = [self.curr_generation[i].copy() for i in range(self.rows)]
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations > self.max_generations  # type: ignore

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r") as fr:
            lines = fr.readlines()
            field = [list(map(int, line)) for line in lines]

        game = GameOfLife((len(field), len(field[0])), False)
        game.curr_generation = [[*line] for line in field]

        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as fw:
            for i in range(self.rows):
                fw.write(" ".join([self.curr_generation[i][j] for j in range(self.cols)]) + "\n")  # type: ignore


if __name__ == "__main__":
    game = GameOfLife((10, 10), max_generations=50)
    for i in range(5):
        print(f"Step: {game.generations}\n")
        pp(game.prev_generation)
        print("-" * 30)
        pp(game.curr_generation)
        print("=" * 30)
        game.step()
