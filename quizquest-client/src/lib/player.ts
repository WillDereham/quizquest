import { goto } from '$app/navigation'
import { get, writable } from 'svelte/store'

interface Player {
  ws: WebSocket
  code: string
  name: string
  status: 'waiting_for_start'
}

export const player = writable<Player | null>(null)

function onMessage(event: MessageEvent) {
  const message = JSON.parse(event.data)
  console.log('Message received:', message)
}

export function joinGame(code: string, name: string) {
  return new Promise((resolve, reject) => {
    console.log({ player: get(player) })
    if (get(player) !== null) {
      return resolve(null)
    }
    const ws = new WebSocket(
      `ws://localhost:8080/join?code=${code}&name=${encodeURIComponent(name)}`,
    )
    player.set({ ws, code, name, status: 'waiting_for_start' })

    const onConnectionError = () => {
      return reject('connection_error')
    }
    const onInitialMessage = (event: MessageEvent) => {
      ws.removeEventListener('message', onInitialMessage)
      ws.removeEventListener('error', onConnectionError)
      const data = JSON.parse(event.data)
      console.log(data)
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
