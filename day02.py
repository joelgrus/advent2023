from dataclasses import dataclass
from typing import List
import re

RAW = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""


@dataclass
class Draw:
    blue: int
    green: int
    red: int

    def possible(self, other: "Draw") -> bool:
        """This is possible if the other draw has at least as many of each color."""
        return (
            self.blue <= other.blue
            and self.green <= other.green
            and self.red <= other.red
        )


@dataclass
class Game:
    id: int
    draws: List[Draw]

    def possible(self, other: Draw) -> bool:
        """This is possible if the other draw is possible for all draws in this game."""
        return all([draw.possible(other) for draw in self.draws])

    def power(self) -> int:
        red = max(draw.red for draw in self.draws)
        blue = max(draw.blue for draw in self.draws)
        green = max(draw.green for draw in self.draws)

        return red * blue * green


def parse_draw(raw: str) -> Draw:
    red_search = re.search(r"(\d+) red", raw)
    blue_search = re.search(r"(\d+) blue", raw)
    green_search = re.search(r"(\d+) green", raw)

    red_count = int(red_search.group(1)) if red_search else 0
    blue_count = int(blue_search.group(1)) if blue_search else 0
    green_count = int(green_search.group(1)) if green_search else 0

    return Draw(red=red_count, blue=blue_count, green=green_count)


def parse(line: str) -> Game:
    id, draws = line.split(":")
    id = int(id.split()[1])
    draws = [parse_draw(raw) for raw in draws.split(";")]
    return Game(id, draws)


GAMES = [parse(line) for line in RAW.split("\n")]
bag = Draw(red=12, green=13, blue=14)
assert (sum(game.id for game in GAMES if game.possible(bag))) == 8
assert (sum(game.power() for game in GAMES)) == 2286

with open("day02.txt") as f:
    raw = f.read()

games = [parse(line) for line in raw.split("\n")]
bag = Draw(red=12, green=13, blue=14)
print(sum(game.id for game in games if game.possible(bag)))
print(sum(game.power() for game in games))
