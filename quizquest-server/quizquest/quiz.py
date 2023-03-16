from __future__ import annotations

from asyncio import get_event_loop
from dataclasses import dataclass, field
from datetime import datetime
from functools import wraps
from random import shuffle, sample
from typing import Self, TypeAlias, Callable, Coroutine, TypeVar, ParamSpec
from uuid import UUID

import firebase_admin
from firebase_admin import firestore
from google.cloud import firestore_v1

from quizquest.utils import asyncify, shuffled

FirestoreDB: TypeAlias = firestore_v1.client.Client


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
    def from_dict(
            cls, quiz_id: str, data: dict, randomise_question_order: bool,
            randomise_answer_order: bool
    ) -> Self:
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
                    ) for answer in (
                        shuffled(question['answers'])
                        if randomise_answer_order else question['answers']
                    )
                ],
            ) for question in (
                shuffled(data['questions']) if randomise_question_order else data['questions']
            )
        ]
        return cls(id=quiz_id, default_time_limit=data['default_time_limit'], questions=questions)


def get_firestore() -> FirestoreDB:
    # TODO: fix blocking calls
    app = firebase_admin.initialize_app()
    db = firestore.client(app)
    return db


def _get_quiz(
        db: FirestoreDB, quiz_id: str, randomise_question_order: bool, randomise_answer_order: bool
) -> Quiz:
    quiz_ref = db.collection('quizzes').document(quiz_id)
    quiz = quiz_ref.get()
    if not quiz.exists:
        raise KeyError("Quiz not found")

    return Quiz.from_dict(
        quiz_id, quiz.to_dict(), randomise_question_order, randomise_answer_order
    )


get_quiz = asyncify(_get_quiz)
