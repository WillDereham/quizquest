from __future__ import annotations

import secrets
from asyncio import sleep, get_running_loop, Future, timeout
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import StrEnum
from math import floor
from typing import TYPE_CHECKING
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
    players_answered: set[UUID] = field(default_factory=set)


@dataclass
class Question:
    id: UUID
    text: str
    answers: list[QuestionAnswer]
    time_limit: int
    player_answers: dict[UUID, tuple[QuestionAnswer, datetime]] = field(default_factory=dict)  # player: answer


class GameStatus(StrEnum):
    waiting_for_start = 'waiting_for_start'
    show_question = 'show_question'
    collect_answers = 'collect_answers'
    question_results = 'question_results'
    game_results = 'game_results'


def _calculate_score(elapsed_time: timedelta, time_limit: timedelta):
    return min(1100 - floor(600 * elapsed_time / time_limit), 1000)


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
            Question(uuid4(), 'What is the derivative of x^2?', [
                QuestionAnswer(uuid4(), 'ln(x)', correct=False),
                QuestionAnswer(uuid4(), '2x^2', correct=False),
                QuestionAnswer(uuid4(), '2x', correct=True),
                QuestionAnswer(uuid4(), 'x^3/3', correct=False),
            ], time_limit=20),
        ]
        self._current_question_id = 0
        self._all_players_answered: Future | None = None

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

    async def start_game(self) -> None:
        await self.start_question()

    async def start_question(self) -> None:
        question = self.current_question

        # Show Question
        self.status = GameStatus.show_question
        self.manager.send_message(Message({
            'type': 'show_question',
            'question': {
                'id': question.id,
                'number': self._current_question_id + 1,
                'text': question.text,
                'answers': [
                    {
                        'id': answer.id, 'text': answer.text, 'correct': answer.correct
                    } for answer in question.answers
                ],
                'time_limit': question.time_limit,
            }
        }))

        show_question_message = Message({
            'type': 'show_question',
            'question': {
                'id': question.id,
                'number': self._current_question_id + 1,
                'answers': [{'id': answer.id} for answer in question.answers]
            },
        })
        for player in self.players.values():
            player.send_message(show_question_message)

        await sleep(5.0)

        # Collect answers
        self.status = GameStatus.collect_answers
        self.manager.send_message(Message({'type': 'collect_answers'}))
        for player in self.players.values():
            player.send_message(Message({'type': 'collect_answers'}))

        start_time = datetime.now(timezone.utc)
        self._all_players_answered = get_running_loop().create_future()
        try:
            async with timeout(question.time_limit):
                await self._all_players_answered
        except TimeoutError:
            pass

        # Question Results
        self.status = GameStatus.question_results

        last_question = self._current_question_id + 1 == len(self.questions)

        for player in self.players.values():
            try:
                (chosen_answer, time_answered) = question.player_answers[player.id]
            except KeyError:
                correct = False
                score_gained = 0
            else:
                correct = chosen_answer.correct
                elapsed_time = time_answered - start_time
                score_gained = _calculate_score(
                    elapsed_time, timedelta(seconds=1) * question.time_limit
                ) if correct else 0

            new_score = player.score = player.score + score_gained
            player.send_message(Message({
                'type': 'question_results',
                'correct': correct,
                'score_gained': score_gained,
                'new_score': new_score,
                'last_question': last_question,
            }))

        self.manager.send_message(Message({
            'type': 'question_results',
            # 'answers': [
            #     {'id': answer.id, 'players_answered': list(answer.players_answered)}
            #     for answer in question.answers
            # ],
            'last_question': last_question,
            'leaderboard': self._get_leaderboard(length=5),
        }))

    def _get_leaderboard(self, length: int):
        return sorted([
            {'id': user.id, 'name': user.name, 'score': user.score}
            for user in self.players.values()
        ], key=lambda u: u['score'], reverse=True)[:length]

    async def next_question(self):
        if self._current_question_id + 1 >= len(self.questions):
            return self.manager.send_error('game_ended')
        self._current_question_id += 1
        await self.start_question()

    async def skip_question(self):
        self._all_players_answered.set_result(None)

    async def game_results(self):
        for index, player in enumerate(sorted(
                self.players.values(), key=lambda p: p.score, reverse=True
        )):
            player.send_message(Message({
                'type': 'game_results',
                'rank': index + 1,
                'score': player.score,
            }))

        self.manager.send_message(Message({
            'type': 'game_results',
            'leaderboard': self._get_leaderboard(length=3),
        }))

    async def on_question_answered(self, player: Player, answer: QuestionAnswer):
        question = self.current_question

        question.player_answers[player.id] = (answer, datetime.now(timezone.utc))
        answer.players_answered.add(player.id)

        # If all players have answered the question
        # Checks if is a superset, because a user could leave before the question is over
        if set(question.player_answers.keys()) >= set(self.players.keys()):
            self._all_players_answered.set_result(None)

        player.send_message(Message({'type': 'question_answered'}))
        # self.manager.send_message(Message({
        #     'type': 'question_answered', 'player_id': player.id, 'answer_id': answer.id
        # }))
