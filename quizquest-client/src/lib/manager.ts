import { goto } from '$app/navigation'
import { PUBLIC_GAME_URL } from '$env/static/public'
import { get, writable } from 'svelte/store'

interface Question {
  id: string
  number: number
  text: string
  answers: { id: string; text: string; correct: boolean }[]
  time_limit: number
}

type GameStatus = 'waiting_for_start' | 'show_question' | 'collect_answers' | 'question_results'
type ShowQuestionStatusUpdate = {
  status: 'show_question'
  question: Question
}
type GameStatusUpdate =
  | { status: 'waiting_for_start' }
  | ShowQuestionStatusUpdate
  | { status: 'collect_answers' }
  | { status: 'question_results' }

export interface Manager {
  ws: WebSocket
  code: string
  players: Map<string, ManagerPlayer>
  status: GameStatus
  current_question: Question | null
}

export interface ManagerPlayer {
  id: string
  name: string
}

export const manager = writable<Manager | null>(null)

function onMessage(event: MessageEvent) {
  const message = JSON.parse(event.data)
  console.debug('Message received:', message)
  switch (message.type) {
    case 'player_joined':
      onPlayerJoin(message)
      break
    case 'player_left':
      onPlayerLeave(message)
      break
    case 'change_status':
      onChangeStatus(message)
      break
    default:
      console.warn('Received unknown message:', message)
  }
}

function onPlayerJoin(message: { player: { id: string; name: string } }) {
  const players = get(manager)?.players
  if (!players) return
  players.set(message.player.id, message.player)
  manager.update((manager) => manager)
}

function onPlayerLeave(message: { player_id: string }) {
  const players = get(manager)?.players
  if (!players) return
  players.delete(message.player_id)
  manager.update((manager) => manager)
}

function onChangeStatus(message: GameStatusUpdate) {
  manager.update((manager) => manager && { ...manager, status: message.status })
  console.log('status changed to', message.status)
  switch (message.status) {
    case 'show_question':
      onShowQuestion(message)
      break
    case 'collect_answers':
      onCollectAnswers(message)
      break
    case 'question_results':
      onQuestionResults(message)
      break
    default:
      console.warn('Unknown game status:', message.status, message)
  }
}

function onShowQuestion(message: ShowQuestionStatusUpdate) {
  manager.update((manager) => manager && { ...manager, current_question: message.question })
  console.log('Show question', message.question)
}

function onCollectAnswers(message: { status: 'collect_answers' }) {
  console.log('Collect answers', message)
}

function onQuestionResults(message: { status: 'question_results' }) {
  console.log('Question results', message)
}

export function startGame() {
  return new Promise((resolve, reject) => {
    console.log({ manager: get(manager) })
    if (get(manager) !== null) {
      return resolve(null)
    }

    const ws = new WebSocket(`${PUBLIC_GAME_URL}/start`)

    const onInitialMessage = (event: MessageEvent) => {
      ws.removeEventListener('message', onInitialMessage)
      const data = JSON.parse(event.data)
      console.log(data)
      if (data.type === 'game_created') {
        ws.addEventListener('message', onMessage)
        manager.set({
          ws,
          code: data.code,
          players: new Map<string, ManagerPlayer>(),
          status: 'waiting_for_start',
          current_question: null,
        })
        return resolve(null)
      } else if (data.type === 'error') {
        return reject(data.code)
      }
      return reject('unknown_error')
    }
    ws.addEventListener('message', onInitialMessage)
    ws.addEventListener('close', () => {
      manager.set(null)
      goto('/')
    })
  })
}

export function kickPlayer(player_id: string) {
  const ws = get(manager)?.ws
  if (!ws) return
  ws.send(JSON.stringify({ type: 'kick_player', player_id }))
}

export function beginGame() {
  const ws = get(manager)?.ws
  if (!ws) return
  ws.send(JSON.stringify({ type: 'start_game' }))
}

export function endGame() {
  get(manager)?.ws.close()
  manager.set(null)
  goto('/')
}
