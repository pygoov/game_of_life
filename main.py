import pygame
import random
import time

from typing import Tuple, Dict, List


def color_smooth(col1: Tuple[int, int, int],
                 col2: Tuple[int, int, int],
                 p: float) -> Tuple[int, int, int]:
    if p < 0:
        p = 0

    if p > 1:
        p = 1

    return (
        int(col1[0] * (1-p) + col2[0] * p),
        int(col1[1] * (1-p) + col2[1] * p),
        int(col1[2] * (1-p) + col2[2] * p),
    )


class Cell:
    def __init__(self, pos: Tuple, is_life: bool) -> None:
        self.pos = pos
        self.color = (0, 0, 0)
        self.is_life = is_life
        self.next_state = False
        self.settime = time.monotonic()

    @property
    def state_time(self) -> float:
        return time.monotonic() - self.settime

    def update(self, map: 'GameMap'):
        xsum = sum([
            map[self.pos[0]-1, self.pos[1]-1],
            map[self.pos[0]-1, self.pos[1]+1],
            map[self.pos[0]+1, self.pos[1]-1],
            map[self.pos[0]+1, self.pos[1]+1],
            map[self.pos[0]-1, self.pos[1]],
            map[self.pos[0], self.pos[1]-1],
            map[self.pos[0], self.pos[1]+1],
            map[self.pos[0]+1, self.pos[1]],
        ])

        if self.is_life:
            if self.state_time < 2:
                self.next_state = xsum in (3, 4, 5, 6)
            elif self.state_time < 3:
                self.next_state = xsum in (3, 4, 5)
            elif self.state_time < 4:
                self.next_state = xsum in (3, 4)
        else:
            if self.state_time < 2:
                self.next_state = xsum in (3, )
            elif self.state_time < 3:
                self.next_state = xsum in (3, 4)
            elif self.state_time < 4:
                self.next_state = xsum in (3, 4, 5)

        if self.next_state != self.is_life:
            self.settime = time.monotonic()

    def draw(self, arr: pygame.PixelArray) -> None:
        arr[self.pos] = self.color  # type: ignore

        self.is_life = self.next_state

        if self.is_life:
            self.color = color_smooth(
                (255, 0, 0),
                (0, 0, 255),
                self.state_time / 5
            )
        else:
            self.color = (0, 0, 0)


class GameMap:

    cells: Dict[int, Dict[int, Cell]]
    cells_arr: List[Cell]

    def __init__(self, size: Tuple[int, int]) -> None:
        self.size = size
        self.cells = {}
        self.cells_arr = []

        for x in range(0, size[0]):
            self.cells[x] = {}
            for y in range(0, size[1]):
                cell = Cell((x, y), random.choice([True, False]))
                self.cells[x][y] = cell
                self.cells_arr.append(cell)

    def __getitem__(self, xy: Tuple[int, int]) -> int:
        x = xy[0]
        if x < 0:
            x = self.size[0] - x
        x = x % self.size[0]

        y = xy[1]
        if y < 0:
            y = self.size[1] - y
        y = y % self.size[1]

        return int(self.cells[x][y].is_life)

    def update(self):
        for cell in self.cells_arr:
            cell.update(self)

    def draw(self, arr: pygame.PixelArray):
        for cell in self.cells_arr:
            cell.draw(arr)


def main():
    pygame.init()
    pygame.display.set_caption("game of life")

    # win_size = (1920, 1080)
    win_size = (640, 480)
    window = pygame.display.set_mode(win_size)

    rs = 5
    game_size = (int(win_size[0]/rs), int(win_size[1]/rs))
    game_map = GameMap(game_size)
    map = pygame.Surface(game_size)

    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

        game_map.update()
        arr = pygame.PixelArray(map)
        game_map.draw(arr)
        del arr
        window.blit(pygame.transform.scale(map, win_size), (0, 0))

        pygame.display.flip()


if __name__ == "__main__":
    main()
