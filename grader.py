import argparse
import sys
import json
from dataclasses import dataclass, asdict
from typing import List, Optional, Union
import datetime
import csv


funny_answers = [[] for i in range(10)]


@dataclass
class FunnyAnswer:
    team: str
    response: str
    answer: str


@dataclass
class WrongAnswer:
    response: str
    answer: str


@dataclass
class AnswerSheet:
    team: str
    round: int
    responses: List[str]
    correct_answers: Optional[List[str]] = None
    wrong_answers: Optional[List[WrongAnswer]] = None


def _get_round_from_row(row):
    return int(row[2].split(" ")[1])


def _get_answers_for_round(round):
    with open("answers.json") as f:
        return json.load(f)[str(round)]


def _naive_grade_answer(response, answers: Union[str, List[str]]):
    if isinstance(answers, str):
        answers = [answers]

    for answer in answers:
        response = response.lower().strip()
        answer = answer.lower().strip()

        if response == answer:
            return True

        if len(response) > 4 and (response in answer or answer in response):
            return True

    return False


def grade_sheet(sheet: AnswerSheet, answers: List[str]):
    correct_answers = []
    wrong_answers = []
    for index, (response, answer) in enumerate(zip(sheet.responses, answers)):
        is_correct = _naive_grade_answer(response, answer)
        if not is_correct:
            grading_response = input(f"Answer: {answer}\nResponse: {response}\n> ")
            if grading_response == "c":
                print("logging correct answer...")
                is_correct = True
            if grading_response == "funny":
                print("logging funny answer....")
                funny_answers[index].append(FunnyAnswer(sheet.team, response, answer))
            print("")

        if is_correct:
            correct_answers.append(response)
        else:
            wrong_answers.append(WrongAnswer(response, answer))

    sheet.correct_answers = correct_answers
    sheet.wrong_answers = wrong_answers
    return sheet


def extract_sheets(round):
    with open("responses.csv") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            if row[2].lower() == "bonus":
                continue
            form_round = _get_round_from_row(row)
            if round != form_round:
                continue

            yield AnswerSheet(team=row[1], round=round, responses=row[3:])


def main(round):
    print("-------------------------")
    print("Press Enter if the answer is wrong.")
    print("Type 'c' if the answer is correct")
    print("Type 'funny' if the answer is wrong but funny.")
    print("-------------------------")
    answers = _get_answers_for_round(round)

    sheets = [grade_sheet(sheet, answers) for sheet in extract_sheets(round)]
    sheets.sort(key=lambda s: s.team)
    print("")
    print("")
    print("RESULTS")
    for sheet in sheets:
        print(f"{sheet.team}: {len(sheet.correct_answers)}")

    jsonified_round = [asdict(sheet) for sheet in sheets]
    filename = f"{round}-{datetime.datetime.now()}.json"
    with open(filename, "w") as f:
        json.dump(jsonified_round, f)

    print("\n\n")
    input("Press enter when you are ready to see the funny answers:\n")

    for i, round in enumerate(funny_answers):
        if not round:
            continue

        print(f"Round: {i + 1}")
        for answer in round:
            print(f"Team: {answer.team}")
            print(f"Expected: {answer.answer}")
            print(f"Response: {answer.response}")
            print("")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--round", choices=[i for i in range(1, 6)], type=int, required=True
    )
    args = parser.parse_args(sys.argv if len(sys.argv) == 1 else None)
    main(args.round)
