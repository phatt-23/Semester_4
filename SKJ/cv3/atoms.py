
import playground
import random

from typing import List, Tuple, NewType

Pos = NewType('Pos', Tuple[int, int])

class Atom:

    def __init__(self, pos: Pos, vel: Pos, rad: int, col: str):
        self.pos = pos
        self.vel = vel
        self.rad = rad
        self.col = col


    def to_tuple(self) -> Tuple[int, int, int, str]:
        return (self.pos[0], self.pos[1], self.rad, self.col)


    def apply_speed(self, size_x: int, size_y: int):
        # print(self.to_tuple())

        x_pos, y_pos = self.pos
        x_vel, y_vel = self.vel


        new_x = x_pos + x_vel
        if new_x > size_x - self.rad or new_x < 0 + self.rad:
            x_vel *= -1


        new_y = y_pos + y_vel
        if new_y > size_y - self.rad or new_y < 0 + self.rad:
            y_vel *= -1
        
        x_pos += x_vel
        y_pos += y_vel

        self.pos = (x_pos, y_pos)
        self.vel = (x_vel, y_vel)


def clamp(x, low, high):
    if x < low:
        return low
    if x > high:
        return high
    return x


class FallDownAtom(Atom):

    def __init__(self, pos: Pos, vel: Pos, rad: int, col: str, g: float = 3.0, damping: float = 0.7):
        super().__init__(pos, vel, rad, col)
        self.g = g
        self.damping = damping


    def apply_speed(self, size_x: int, size_y: int):
        x_pos, y_pos = self.pos
        x_vel, y_vel = self.vel

        new_x = x_pos + x_vel
        if new_x > size_x - self.rad or new_x < 0 + self.rad:
            x_vel *= -1 * self.damping


        y_vel += self.g
        new_y = y_pos + y_vel
        if new_y > size_y - self.rad or new_y < 0 + self.rad:
            y_vel *= -1 * self.damping

        
        
        self.pos = (clamp(new_x, 0 + self.rad, size_x - self.rad), clamp(new_y, 0 + self.rad, size_y - self.rad))
        self.vel = (x_vel, y_vel)


class ExampleWorld:

    def __init__(self, size_x: int, size_y: int, no_atoms: int, no_falldown_atoms: int):
        self.width = size_x
        self.height = size_y
        self.atoms = self.generate_atoms(no_atoms, no_falldown_atoms)


    def generate_atoms(self, no_atoms: int, no_falldown_atoms) -> List[Atom]:
        return [self.random_atom() for _ in range(no_atoms)] + [self.random_falldown_atom() for _ in range(no_falldown_atoms)]


    def random_atom_spec(self) -> Tuple[Pos, Pos, int]:
        speed = 30
        vel_x = int(speed * (random.random() - 0.5))
        vel_y = int(speed * (random.random() - 0.5))

        radius = clamp(int(30 * random.random()), 10, 100)

        pos_x = clamp(int(self.width * random.random()), radius, self.width - radius)
        pos_y = clamp(int(self.height * random.random()), radius, self.height - radius)

        return (Pos((pos_x, pos_y)), Pos((vel_x, vel_y)), radius)


    def random_atom(self) -> Atom:
        color = 'green'

        args = self.random_atom_spec()
        return Atom(*args, color)


    def random_falldown_atom(self) -> FallDownAtom:
        color = 'yellow'

        args = self.random_atom_spec()
        return FallDownAtom(*args, color);


    def add_atom(self, pos_x, pos_y):
        color = 'green'

        _, vel, rad = self.random_atom_spec()
        self.atoms.append(Atom(Pos((pos_x, pos_y)), vel, rad, color))


    def add_falldown_atom(self, pos_x, pos_y) -> None:
        color = 'yellow'

        _, vel, rad = self.random_atom_spec()
        self.atoms.append(FallDownAtom(Pos((pos_x, pos_y)), vel, rad, color))


    def tick(self):
        for a in self.atoms:
            a.apply_speed(self.width, self.height)

        return (*(a.to_tuple() for a in self.atoms), )


if __name__ == '__main__':
    size_x, size_y = 700, 400
    no_atoms = 4
    no_falldown_atoms = 4

    world = ExampleWorld(size_x, size_y, no_atoms, no_falldown_atoms)

    playground.run((size_x, size_y), world)


