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
      get(manager)?.players.set(message.player.name, message.player)
      manager.update((manager) => manager)
      console.log(get(manager)?.players)
      break
    case 'player_left':
      break
    default:
      console.warn('Received unknown message:', message)
  }
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

export function endGame() {
  get(manager)?.ws.close()
  manager.set(null)
  goto('/')
}
