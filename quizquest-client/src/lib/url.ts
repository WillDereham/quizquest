import { page } from '$app/stores'
import { get } from 'svelte/store'

export function getJoinUrl(code: string) {
  return `${get(page).url.origin}/join?code=${code}`
}
