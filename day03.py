from typing import NamedTuple, List, Dict
from dataclasses import dataclass
import re


RAW = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


class XY(NamedTuple):
    x: int
    y: int


@dataclass
class Number:
    start: XY
    end: XY
    value: int


def is_adjacent(symbol_location: Number, number: Number) -> bool:
    nxlo, nxhi = number.start.x, number.end.x
    ny = number.start.y

    x, y = symbol_location

    return nxlo - 1 <= x <= nxhi + 1 and ny - 1 <= y <= ny + 1


@dataclass
class Schematic:
    numbers: List[Number]
    symbols: Dict[XY, str]

    def part_numbers(self) -> List[int]:
        return [
            number.value for number in self.numbers if self.adjacent_to_symbol(number)
        ]

    def adjacent_to_symbol(self, number: Number) -> bool:
        return any(
            is_adjacent(symbol_location, number) for symbol_location in self.symbols
        )

    def gear_ratios(self) -> List[int]:
        output: List[int] = []
        candidate_locs = [loc for loc, symbol in self.symbols.items() if symbol == "*"]

        for loc in candidate_locs:
            adjacent_numbers = [n for n in self.numbers if is_adjacent(loc, n)]
            if len(adjacent_numbers) == 2:
                output.append(adjacent_numbers[0].value * adjacent_numbers[1].value)

        return output


def parse(raw: str) -> Schematic:
    lines = raw.splitlines()
    numbers = []
    symbols = {}
    for y, line in enumerate(lines):
        # handle numbers
        for match in re.finditer(r"\d+", line):
            start = XY(match.start(), y)
            end = XY(match.end() - 1, y)
            numbers.append(Number(start, end, int(match.group())))

        # handle symbols
        for x, symbol in enumerate(line):
            if not symbol.isdigit() and symbol != ".":
                symbols[XY(x, y)] = symbol

    return Schematic(numbers, symbols)


SCHEMATIC = parse(RAW)
assert sum(SCHEMATIC.part_numbers()) == 4361
assert sum(SCHEMATIC.gear_ratios()) == 467835

with open("day03.txt") as f:
    schematic = parse(f.read())

print(sum(schematic.part_numbers()))
print(sum(schematic.gear_ratios()))
