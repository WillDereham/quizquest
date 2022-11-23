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
type ShowQuestionMessage = {
  type: 'show_question'
  question: Question
}

export interface Manager {
  ws: WebSocket
  code: string
  players: Map<string, ManagerPlayer>
  status: GameStatus
  current_question: Question | null
  question_results: { last_question: boolean } | null
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

function changeStatus(status: GameStatus) {
  manager.update((manager) => manager && { ...manager, status })
  console.log('status changed to', status)
}

function onShowQuestion(message: ShowQuestionMessage) {
  changeStatus('show_question')
  manager.update((manager) => manager && { ...manager, current_question: message.question })
  console.log('Show question', message.question)
}

function onCollectAnswers(message: { type: 'collect_answers' }) {
  changeStatus('collect_answers')
  console.log('Collect answers', message)
}

function onQuestionResults(message: { type: 'question_results'; last_question: boolean }) {
  changeStatus('question_results')
  manager.update(
    (manager) =>
      manager && { ...manager, question_results: { last_question: message.last_question } },
  )

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
          question_results: null,
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

function sendMessage(message: unknown) {
  const ws = get(manager)?.ws
  if (!ws) return
  ws.send(JSON.stringify(message))
}

export function kickPlayer(player_id: string) {
  sendMessage({ type: 'kick_player', player_id })
}

export function beginGame() {
  sendMessage({ type: 'start_game' })
}

export function nextQuestion() {
  sendMessage({ type: 'next_question' })
}

export function endGame() {
  get(manager)?.ws.close()
  manager.set(null)
  goto('/')
}
