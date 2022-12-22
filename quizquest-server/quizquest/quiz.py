from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from functools import lru_cache
from typing import Self
from uuid import UUID

import firebase_admin
from firebase_admin import firestore
from google.cloud import firestore_v1


@dataclass
class QuestionAnswer:
    id: UUID
    text: str
    correct: bool
    players_answered: set[UUID] = field(default_factory=set)


@dataclass
class Question:
    id: UUID
    text: str
    answers: list[QuestionAnswer]
    time_limit: int | None
    player_answers: dict[UUID, tuple[QuestionAnswer, datetime]] = field(default_factory=dict)  # player_id: answer


@dataclass
class Quiz:
    id: str
    default_time_limit: int
    questions: list[Question]

    @classmethod
    def from_dict(cls, quiz_id: str, data: dict) -> Self:
        questions = [
            Question(
                id=UUID(question['id']),
                text=question['text'],
                time_limit=question['time_limit'],
                answers=[
                    QuestionAnswer(
                        id=UUID(answer['id']),
                        text=answer['text'],
                        correct=answer['correct'],
                    ) for answer in question['answers']
                ],
            ) for question in data['questions']
        ]
        return cls(id=quiz_id, default_time_limit=data['default_time_limit'], questions=questions)


# executor = ThreadPoolExecutor(max_workers=4)


@lru_cache(maxsize=1)
def get_firestore() -> firestore_v1.client.Client:
    # TODO: fix blocking calls
    app = firebase_admin.initialize_app()
    db = firestore.client(app)
    return db


def get_quiz(quiz_id: str):
    db = get_firestore()
    quiz_ref = db.collection('quizzes').document(quiz_id)
    quiz = quiz_ref.get()
    if not quiz.exists:
        raise KeyError("Quiz not found")

    return Quiz.from_dict(quiz_id, quiz.to_dict())
