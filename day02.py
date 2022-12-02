from enum import Enum


class Shape(Enum):
    ROCK = "Rock"
    PAPER = "Paper"
    SCISSORS = "Scissors"

    @staticmethod
    def from_short_string(s):
        if s in ["A", "X"]:
            return Shape.ROCK
        elif s in ["B", "Y"]:
            return Shape.PAPER
        elif s in ["C", "Z"]:
            return Shape.SCISSORS
        else:
            raise f"Unknown string shape '{s}'"


class Result(Enum):
    WIN = "win"
    DRAW = "draw"
    LOOSE = "loose"


def play(shape1, shape2):
    # Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock.
    # If both players choose the same shape, the round instead ends in a draw.
    if (shape1 == Shape.ROCK and shape2 == Shape.SCISSORS) or \
            (shape1 == Shape.SCISSORS and shape2 == Shape.PAPER) or \
            (shape1 == Shape.PAPER and shape2 == Shape.ROCK):
        return Result.WIN
    elif shape1 == shape2:
        return Result.DRAW
    else:
        return Result.LOOSE


def test_play():
    assert play(Shape.ROCK, Shape.SCISSORS) == Result.WIN
    assert play(Shape.ROCK, Shape.PAPER) == Result.LOOSE
    assert play(Shape.ROCK, Shape.ROCK) == Result.DRAW
    assert play(Shape.SCISSORS, Shape.SCISSORS) == Result.DRAW
    assert play(Shape.SCISSORS, Shape.PAPER) == Result.WIN
    assert play(Shape.SCISSORS, Shape.ROCK) == Result.LOOSE
    assert play(Shape.PAPER, Shape.SCISSORS) == Result.LOOSE
    assert play(Shape.PAPER, Shape.PAPER) == Result.DRAW
    assert play(Shape.PAPER, Shape.ROCK) == Result.WIN


def points_for_shape(shape):
    points = {Shape.ROCK: 1, Shape.PAPER: 2, Shape.SCISSORS: 3}
    return points[shape]


def points_for_play(play_result):
    points = {Result.LOOSE: 0, Result.DRAW: 3, Result.WIN: 6}
    return points[play_result]


def main(file):
    part1(file)


def part1(file):
    with open(file, "r") as f:
        total_score = 0

        for line in f.readlines():
            line = line.replace("\n", "")
            (opponent_s, me_s) = line.split(' ')
            opponent = Shape.from_short_string(opponent_s)
            me = Shape.from_short_string(me_s)
            outcome = play(me, opponent)
            shape_points = points_for_shape(me)
            outcome_points = points_for_play(outcome)
            total_score = total_score + shape_points + outcome_points

        print(total_score)


if __name__ == "__main__":
    main("input02.txt")
