import argparse
import sys
import json
from dataclasses import dataclass
from typing import List
import csv


round_cache = {}


@dataclass
class RoundResult:
    team: str
    round: int
    score: int
    wrong_answers: List


def _get_round_from_row(row):
    return int(row[2].split(" ")[1])


def _get_answers_for_round(round):
    if round in round_cache:
        return round_cache[round]

    with open("answers.json") as f:
        answers = json.load(f)[str(round)]
        round_cache[round] = answers
        return answers


def grade_round(row) -> RoundResult:
    team = row[1]
    round = _get_round_from_row(row)
    responses = row[3:]
    correct_answers = _get_answers_for_round(round)

    score = 0
    wrong_answers = []
    for response, correct in zip(responses, correct_answers):
        is_correct = response.lower() == correct.lower()

        if is_correct:
            score += 1
        else:
            wrong_answers.append((response, correct))

    return RoundResult(team, round, score, wrong_answers)


def format_round(result: RoundResult):
    print(f"Team: {result.team}")
    print(f"Round: {result.round}")
    print(f"Score: {result.score}")
    print("Wrong answers:")
    for res, expected in result.wrong_answers:
        print(f"{res}\t{expected}")
    print("")


def extract_responses():
    with open("responses.csv") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            yield row


def main(args):
    grading_round = args.round
    for row in extract_responses():
        round = _get_round_from_row(row)
        if round != grading_round:
            continue
        score = grade_round(row)
        format_round(score)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--round", choices=[i for i in range(1, 6)], type=int, required=True
    )
    args = parser.parse_args(sys.argv if len(sys.argv) == 1 else None)
    main(args)

# input team answers

# get score, and wrong answers
