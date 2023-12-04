from dataclasses import dataclass
from typing import List

RAW = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


@dataclass
class Card:
    id: int
    winning_numbers: List[int]
    numbers_you_have: List[int]

    def num_matches(self) -> int:
        winners = set(self.winning_numbers)
        num_matches = sum(n in winners for n in self.numbers_you_have)

        return num_matches

    def score(self) -> int:
        num_matches = self.num_matches()

        if num_matches == 0:
            return 0
        else:
            return 2 ** (num_matches - 1)


def parse(line: str) -> Card:
    id, numbers = line.split(":")
    id = int(id.split()[1])

    winning_numbers, numbers_you_have = numbers.split("|")
    winning_numbers = [int(n) for n in winning_numbers.split()]
    numbers_you_have = [int(n) for n in numbers_you_have.split()]

    return Card(id, winning_numbers, numbers_you_have)


CARDS = [parse(line) for line in RAW.splitlines()]
assert sum(card.score() for card in CARDS) == 13

with open("day04.txt") as f:
    cards = [parse(line) for line in f]

print(sum(card.score() for card in cards))


def count_cards(cards: List[Card]) -> int:
    counts = [1 for card in cards]

    for i, card in enumerate(cards):
        num_copies = counts[i]
        num_matches = card.num_matches()

        for di in range(num_matches):
            counts[i + di + 1] += num_copies

    return sum(counts)


assert count_cards(CARDS) == 30
print(count_cards(cards))
