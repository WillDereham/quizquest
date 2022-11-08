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
  const data = JSON.parse(event.data)
  console.log('Message received:', data)
}

export function joinGame(code: string, name: string) {
  return new Promise((resolve, reject) => {
    console.log({ player: get(player) })
    if (get(player) !== null) {
      resolve(null)
    }
    const ws = new WebSocket(
      `ws://localhost:8080/join?code=${code}&name=${encodeURIComponent(name)}`,
    )
    player.set({ ws, code, name, status: 'waiting_for_start' })

    const onInitialMessage = (event: MessageEvent) => {
      ws.removeEventListener('message', onInitialMessage)
      const data = JSON.parse(event.data)
      console.log(data)
      if (data.type === 'connected') {
        ws.addEventListener('message', onMessage)
        resolve(null)
      } else if (data.type === 'error') {
        reject(data.code)
      }
      reject('unknown_error')
    }
    ws.addEventListener('message', onInitialMessage)
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
