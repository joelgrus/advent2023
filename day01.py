import re


RAW = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""


def calibration_value(line: str) -> int:
    digits = [int(c) for c in line if c.isdigit()]
    return 10 * digits[0] + digits[-1]


assert calibration_value("1abc2") == 12
assert calibration_value("pqr3stu8vwx") == 38
assert calibration_value("a1b2c3d4e5f") == 15
assert calibration_value("treb7uchet") == 77

with open("day01.txt") as f:
    lines = f.readlines()

print(sum(calibration_value(line) for line in lines))

rgx = r"[0-9]|one|two|three|four|five|six|seven|eight|nine"
back_rgx = r"enin|thgie|neves|xis|evif|ruof|eerht|owt|eno|[0-9]"


def digit_value(s: str) -> int:
    if s.isdigit():
        return int(s)
    else:
        return {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
            # also include backwards
            "eno": 1,
            "owt": 2,
            "eerht": 3,
            "ruof": 4,
            "evif": 5,
            "xis": 6,
            "neves": 7,
            "thgie": 8,
            "enin": 9,
        }[s]


assert digit_value("1") == 1
assert digit_value("one") == 1


def calibration_value2(line: str) -> int:
    first_value = digit_value(re.search(rgx, line).group())
    last_value = digit_value(re.search(back_rgx, line[::-1]).group())

    return 10 * first_value + last_value


assert calibration_value2("1abc2") == 12
assert calibration_value2("pqr3stu8vwx") == 38
assert calibration_value2("a1b2c3d4e5f") == 15
assert calibration_value2("treb7uchet") == 77
assert calibration_value2("one1two2three3four4five5six6seven7eight") == 18
assert calibration_value2("oneight") == 18

print(sum(calibration_value2(line) for line in lines))
