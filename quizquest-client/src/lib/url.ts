import { page } from '$app/stores'
import { get } from 'svelte/store'
import QRCode from 'qrcode'

export function getJoinUrl(code: string) {
  return `${get(page).url.origin}/join?code=${code}`
}

export async function getQRCodeURL(code: string) {
  return await QRCode.toDataURL(getJoinUrl(code), { margin: 2, scale: 8 })
}
