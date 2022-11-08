import { goto } from '$app/navigation'
import { get, writable } from 'svelte/store'

interface Manager {
  ws: WebSocket
  code: string
  players: Map<string, ManagerPlayer>
  status: 'waiting_for_start'
}

interface ManagerPlayer {
  name: string
}

export const manager = writable<Manager | null>(null)

function onMessage(event: MessageEvent) {
  const data = JSON.parse(event.data)
  console.log('Message received:', data)
}

export function startGame() {
  return new Promise((resolve, reject) => {
    console.log({ manager: get(manager) })
    if (get(manager) !== null) {
      resolve(null)
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
        resolve(null)
      } else if (data.type === 'error') {
        reject(data.code)
      }
      reject('unknown_error')
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
