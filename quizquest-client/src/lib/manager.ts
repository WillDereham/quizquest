import { goto } from '$app/navigation'
import { get, writable } from 'svelte/store'

export interface Manager {
  ws: WebSocket
  code: string
  players: Map<string, ManagerPlayer>
  status: 'waiting_for_start'
}

export interface ManagerPlayer {
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
    default:
      console.warn('Received unknown message:', message)
  }
}

function onPlayerJoin(message: { player: { name: string } }) {
  const players = get(manager)?.players
  if (!players) return
  players.set(message.player.name, message.player)
  manager.update((manager) => manager)
}

function onPlayerLeave(message: { name: string }) {
  const players = get(manager)?.players
  if (!players) return
  players.delete(message.name)
  manager.update((manager) => manager)
}

export function startGame() {
  return new Promise((resolve, reject) => {
    console.log({ manager: get(manager) })
    if (get(manager) !== null) {
      return resolve(null)
    }
    const ws = new WebSocket('ws://localhost:8080/start')

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

export function kickPlayer(name: string) {
  const ws = get(manager)?.ws
  if (!ws) return
  ws.send(JSON.stringify({ type: 'kick_player', name }))
}

export function endGame() {
  get(manager)?.ws.close()
  manager.set(null)
  goto('/')
}
