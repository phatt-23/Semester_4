import time
from enum import StrEnum
from typing import Any, Callable, Generic, List, Tuple, TypeVar
from itertools import chain
from dataclasses import dataclass


class Vector:
    x: float
    y: float
    z: float

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise ValueError
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise ValueError
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __getitem__(self, index: int):
        match index:
            case 0:
                return self.x
            case 1:
                return self.y
            case 2:
                return self.z
            case _:
                raise IndexError

    def __setitem__(self, index: int, value):
        if type(self.x) is not type(value):
            raise TypeError

        match index:
            case 0:
                self.x = value
            case 1:
                self.y = value
            case 2:
                self.z = value
            case _:
                raise IndexError

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z


class Observable:
    _subscribers: List[Callable[[Any], Any]]

    def __init__(self):
        self._subscribers = []

    def subscribe(self, subscriber: Callable):
        self._subscribers.append(subscriber)
        return lambda: self._subscribers.remove(subscriber)

    def notify(self, *args, **kwargs):
        for subscriber in self._subscribers:
            subscriber(*args, **kwargs)


open("file.txt", "w")


class UpperCaseDecorator:
    def __init__(self, file):
        self.file = file

    def write(self, text: str):
        text = "".join([c for c in text if not str.isupper(c)]).upper()
        print(text)
        self.file.write(text)

    def writelines(self, lines: List[str]):
        for line in lines:
            self.write(line)


###########################################################################
#### Game of Life #########################################################
###########################################################################

T = TypeVar("T")

@dataclass
class Vec2(Generic[T]):
    x: int
    y: int 

    def __hash__(self) -> int:
        return tuple.__hash__((self.x, self.y))

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y

    def __gt__(self, other):
        return self.x > other.x and self.y > other.y

    def __le__(self, other):
        return self.x <= other.x and self.y <= other.y

    def __ge__(self, other):
        return self.x >= other.x and self.y >= other.y


Vec2i = Vec2[int]


CellState = StrEnum("CellState", [("ALIVE", "x"), ("DEAD", ".")])


@dataclass
class BoardCell:
    state: CellState
    pos: Vec2i


class GameBoard:
    width: int
    height: int
    board: Tuple[Tuple[BoardCell, ...], ...]

    def __init__(self, board: Tuple[Tuple[str, ...], ...]):
        self.width = len(board[0])
        self.height = len(board)

        # the resource is cloned by this also
        self.board = tuple(
            tuple(
                BoardCell(CellState(symbol), Vec2i(col_i, row_i)) 
                for col_i, symbol in enumerate(row)
            ) 
            for row_i, row in enumerate(board)
        )

    def __repr__(self):
        return "\n".join("".join(cell.state.value for cell in row) for row in self.board) + "\n"

    def __iter__(self):
        return iter(self.board)

    def flat(self):
        return chain.from_iterable(self.board)

    def clone(self):
        raw_board = tuple(tuple(cell.state.value for cell in row) for row in self.board)
        return GameBoard(raw_board)

    def raw(self):
        return tuple(tuple(cell.state.value for cell in row) for row in self.board)

    def as_dict(self):
        return {cell.pos: cell for cell in self.flat()}

    def alive_neighbor_count(self, cell: BoardCell):
        neighbors = (Vec2i(n[0], n[1]) for n in (
            (-1, -1), (0, -1), (1, -1),
            (-1,  0),          (1,  0),
            (-1,  1), (0,  1), (1,  1),
        ))
        
        current_board = self.as_dict()

        alive_count = 0
        for n in neighbors:
            pos = cell.pos + n
            if not (pos >= Vec2i(0, 0) and pos < Vec2i(self.width, self.height)):
                continue
            if current_board[pos].state == CellState.ALIVE:
                alive_count += 1

        return alive_count


class GameOfLife:
    game_board: GameBoard

    def __init__(self, board: Tuple[Tuple[str, ...], ...]):
        self.game_board = GameBoard(board)

    @property
    def board(self):
        return self.game_board.raw()

    def move(self):
        cur_board = self.game_board
        new_board = self.game_board.clone()
        new_board_dict = new_board.as_dict()

        for cell in cur_board.flat():
            alive_count = cur_board.alive_neighbor_count(cell)
            match alive_count:
                case a if a < 2 or a > 3:
                    new_board_dict[cell.pos].state = CellState.DEAD

                case a if a == 3 and cell.state == CellState.DEAD:
                    new_board_dict[cell.pos].state = CellState.ALIVE

        return GameOfLife(new_board.raw())

    def alive(self):
        return len([1 for c in self.game_board.flat() if c.state == CellState.ALIVE])

    def dead(self):
        return len([1 for c in self.game_board.flat() if c.state == CellState.DEAD])

    def __repr__(self):
        return self.game_board.__repr__()


def play_game(game: GameOfLife, n: int):
    for _ in range(n):
        print(game)
        game = game.move()
        time.sleep(0.25)


if __name__ == "__main__":
    board = (
        (".", ".", "."),
        (".", "x", "."),
        (".", "x", "."),
        (".", "x", "."),
        (".", ".", "."),
    )

    game = GameOfLife(board)
    play_game(game, 10)

