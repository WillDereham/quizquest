from __future__ import annotations

import secrets
from asyncio import sleep, get_running_loop, Future, timeout
from dataclasses import dataclass, field
from enum import StrEnum
from typing import TYPE_CHECKING, Callable
from uuid import UUID, uuid4

from quizquest.message import Message

if TYPE_CHECKING:
    from quizquest.manager import Manager
    from quizquest.player import Player

games = {}


@dataclass
class QuestionAnswer:
    id: UUID
    text: str
    correct: bool


@dataclass
class Question:
    id: UUID
    text: str
    answers: list[QuestionAnswer]
    time_limit: int
    received_answers: dict[UUID, UUID] = field(default_factory=dict)  # player_id: answer_id


class GameStatus(StrEnum):
    waiting_for_start = 'waiting_for_start'
    show_question = 'show_question'
    collect_answers = 'collect_answers'
    question_results = 'question_results'


class Game:
    def __init__(self) -> None:
        self.code = secrets.randbelow(900000) + 100000
        self.manager: Manager | None = None
        self.players: dict[UUID, Player] = {}
        self.status = 'waiting_for_start'
        self.questions: list[Question] = [
            Question(uuid4(), 'What is 2 + 2?', [
                QuestionAnswer(uuid4(), '1', correct=False),
                QuestionAnswer(uuid4(), '20', correct=False),
                QuestionAnswer(uuid4(), '4', correct=True),
                QuestionAnswer(uuid4(), '-1', correct=False),
                QuestionAnswer(uuid4(), '5', correct=False),
                QuestionAnswer(uuid4(), '5', correct=False),
            ], time_limit=10),
            Question(uuid4(), 'What is the derivative of ln x?', [
                QuestionAnswer(uuid4(), 'ln(ln(x)', correct=False),
                QuestionAnswer(uuid4(), 'x^2', correct=False),
                QuestionAnswer(uuid4(), 'x^x', correct=False),
                QuestionAnswer(uuid4(), '1/x', correct=True),
            ], time_limit=20),
        ]
        self._current_question_id = 0
        self.all_players_answered: Future | None = None

    @property
    def current_question(self) -> Question:
        return self.questions[self._current_question_id]

    def on_player_leave(self, player_id: UUID) -> None:
        self.manager.send_message(Message({'type': 'player_left', 'player_id': player_id}))
        del self.players[player_id]

    def on_player_join(self, player: Player) -> None:
        self.players[player.id] = player
        self.manager.send_message(
            Message({'type': 'player_joined', 'player': {'id': player.id, 'name': player.name}})
        )

    async def kick_player(self, player_id: UUID) -> None:
        try:
            player = self.players[player_id]
        except KeyError:
            return

        player.send_message(Message({'type': 'player_kicked'}))
        await player.disconnect()

    def _change_status(
            self,
            status: GameStatus,
            manager_data: dict,
            player_data: Callable[[Player], dict],
    ):
        self.status = status
        self.manager.send_message(Message({
            'type': 'change_status',
            'status': status,
            **manager_data,

        }))
        for player in self.players.values():
            player.send_message(Message({
                'type': 'change_status',
                'status': status,
                **player_data(player),
            }))

    async def start_question(self) -> None:
        question = self.current_question
        self._change_status(
            GameStatus.show_question,
            manager_data={'question': {
                'id': question.id,
                'number': self._current_question_id + 1,
                'text': question.text,
                'answers': [
                    {
                        'id': answer.id, 'text': answer.text, 'correct': answer.correct
                    } for answer in question.answers
                ],
                'time_limit': question.time_limit,
            }},
            player_data=lambda p: {},
        )
        await sleep(5)
        self._change_status(
            GameStatus.collect_answers,
            manager_data={},
            player_data=lambda p: {'number_of_answers': len(question.answers)},
        )
        loop = get_running_loop()
        self.all_players_answered = loop.create_future()
        try:
            async with timeout(question.time_limit):
                await self.all_players_answered
        except TimeoutError:
            pass

        # Collect answers
        self._change_status(GameStatus.question_results, manager_data={
            # Score details
        }, player_data=lambda p: {})

    async def on_question_answered(self, player_id: UUID, answer_id: UUID):
        question = self.current_question
        question.received_answers[player_id] = answer_id

        # If all players have answered the question
        # Checks if is a superset, because a user could leave before the question is over
        if set(question.received_answers.keys()) >= set(self.players.keys()):
            self.all_players_answered.set_result(None)

        self.manager.send_message(Message({
            'type': 'question_answered', 'player_id': player_id, 'answer_id': answer_id
        }))
