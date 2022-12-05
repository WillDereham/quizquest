import { goto } from '$app/navigation'
import { PUBLIC_GAME_URL } from '$env/static/public'
import { get, writable } from 'svelte/store'

type GameStatus =
  | 'waiting_for_start'
  | 'show_question'
  | 'collect_answers'
  | 'question_answered'
  | 'question_results'

interface Question {
  id: string
  number: number
  answers: { id: string }[]
}

interface Player {
  ws: WebSocket
  code: string
  name: string
  status: GameStatus
  current_question: Question | null
  question_results: {
    correct: boolean
    score_gained: number
    last_question: boolean
  } | null
  score: number
}

export const player = writable<Player | null>(null)

function onMessage(event: MessageEvent) {
  const message = JSON.parse(event.data)
  console.log('Message received:', message)
  switch (message.type) {
    case 'show_question':
      onShowQuestion(message)
      break
    case 'collect_answers':
      onCollectAnswers(message)
      break
    case 'question_answered':
      onQuestionAnswered(message)
      break
    case 'question_results':
      onQuestionResults(message)
      break

    default:
      console.warn('Received unknown message:', message)
  }
}

function changeStatus(status: GameStatus) {
  player.update((player) => player && { ...player, status })
  console.log('status changed to', status)
}

function onShowQuestion(message: { type: 'show_question'; question: Question }) {
  changeStatus('show_question')
  player.update((player) => player && { ...player, current_question: message.question })
  console.log('Show question', message.question)
}

function onCollectAnswers(message: { type: 'collect_answers' }) {
  changeStatus('collect_answers')
  console.log('Collect answers', message)
}

function onQuestionAnswered(message: { type: 'question_answered' }) {
  changeStatus('question_answered')
  console.log('Question answered', message)
}

function onQuestionResults(message: {
  type: 'question_results'
  correct: boolean
  score_gained: number
  new_score: number
  last_question: boolean
}) {
  changeStatus('question_results')
  player.update(
    (player) =>
      player && {
        ...player,
        question_results: {
          correct: message.correct,
          score_gained: message.score_gained,
          last_question: message.last_question,
        },
        score: message.new_score,
      },
  )
  console.log('Question results', message)
}

export function answerQuestion(answer_id: string) {
  const ws = get(player)?.ws
  if (!ws) return
  ws.send(JSON.stringify({ type: 'answer_question', answer_id }))
}

export function joinGame(code: string, name: string) {
  return new Promise((resolve, reject) => {
    console.log('joining game', { player: get(player) })
    if (get(player) !== null) {
      console.log('Already in a game', get(player))
      return resolve(null)
    }
    const ws = new WebSocket(
      `${PUBLIC_GAME_URL}/join?code=${code}&name=${encodeURIComponent(name)}`,
    )
    player.set({
      ws,
      code,
      name,
      status: 'waiting_for_start',
      current_question: null,
      question_results: null,
      score: 0,
    })

    const onConnectionError = () => {
      return reject('connection_error')
    }
    const onInitialMessage = (event: MessageEvent) => {
      ws.removeEventListener('message', onInitialMessage)
      ws.removeEventListener('error', onConnectionError)
      const data = JSON.parse(event.data)
      console.log('received initial message', data)
      if (data.type === 'connected') {
        ws.addEventListener('message', onMessage)
        return resolve(null)
      } else if (data.type === 'error') {
        return reject(data.code)
      }
      return reject('unknown_error')
    }
    ws.addEventListener('message', onInitialMessage)
    ws.addEventListener('error', onConnectionError)
    ws.addEventListener('close', () => {
      console.log('Connection closed')
      player.set(null)
      goto('/join')
    })
  })
}

export function leaveGame() {
  get(player)?.ws.close()
  player.set(null)
  goto('/join')
}
