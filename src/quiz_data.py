import json
import random


def load_questions(filepath="questions.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def get_question(questions, index):
    if 0 <= index < len(questions):
        return questions[index]
    return None


def get_question_by_id(questions, question_id):
    for q in questions:
        if q.get("id") == question_id:
            return q
    return None


def shuffle_questions(questions):
    shuffled = questions.copy()
    random.shuffle(shuffled)
    return shuffled
