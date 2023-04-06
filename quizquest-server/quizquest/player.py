from __future__ import annotations

from string import ascii_lowercase
from unicodedata import normalize
from uuid import uuid4, UUID

from websockets.legacy.server import WebSocketServerProtocol

from quizquest.client import Client, require_game_status
from quizquest.message import Message

from quizquest.game import Game, GameStatus


def validate_name(name: str) -> bool:
    if len(name) > 16 or len(name) == 0:
        return False

    name = normalize('NFD', name).lower()
    name = ''.join([letter for letter in name if letter in ascii_lowercase])
    words = {word for word in banned_words if word in name}
    return not len(words)


def get_banned_words() -> set[str]:
    with open('banned_words.txt', 'r') as f:
        return {word.strip() for word in f.readlines()}


banned_words = get_banned_words()


class Player(Client):
    def __init__(self, ws: WebSocketServerProtocol, game: Game, name: str) -> None:
        super().__init__(ws, game)
        self.id = uuid4()
        self.name = name
        self.score = 0

    async def handle_incoming_message(self, message: Message) -> None:
        print(f"player '{self.name}' handling message: '{message}'")
        match message.type:
            case 'answer_question':
                await self.handle_answer_question(message)
            case _:
                self.send_error('invalid_message')

    @require_game_status(GameStatus.collect_answers)
    async def handle_answer_question(self, message: Message) -> None:
        try:
            answer_id = UUID(message['answer_id'])
        except (KeyError, ValueError):
            return self.send_error('invalid_answer_id')

        question = self.game.current_question
        if self.id in question.player_answers:
            return self.send_error('already_answered')
        # TODO: use ordereddict for question.answers
        answer = next(
            (answer for answer in question.answers if answer.id == answer_id),
            None
        )
        if answer is None:
            return self.send_error('invalid_answer_id')

        self.game.on_question_answered(self, answer)
