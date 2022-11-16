<script lang="ts">
  import { goto } from '$app/navigation'
  import { player, joinGame } from '$lib/player'
  import { onMount } from 'svelte'
  import Fa from 'svelte-fa'
  import { faArrowLeft } from '@fortawesome/free-solid-svg-icons'
  import { page } from '$app/stores'

  let code = $page.url.searchParams.get('code') || ''
  $: code = code.replaceAll(/\D+/g, '').substring(0, 6)
  let name = ''
  $: name = name.substring(0, 16)
  let loading = false
  let error: string | null = null

  async function onJoin() {
    loading = true
    error = null
    try {
      await joinGame(code, name)
      goto('/play')
    } catch (e: unknown) {
      error = e as string
    } finally {
      loading = false
    }
  }

  onMount(() => {
    if ($player !== null) {
      goto('/play')
    }
  })
</script>

<div class="h-full flex flex-col">
  <div class="flex">
    <a href="/" class="p-6"><Fa icon={faArrowLeft} size="lg" /></a>
  </div>
  <div class="flex items-center justify-center grow">
    <div class="flex flex-col items-center p-4 gap-4">
      {#if loading}
        <div>Loading...</div>
      {:else}
        <h1 class="text-4xl">Join Game</h1>
        <form class="flex flex-col gap-4 items-center" on:submit={onJoin}>
          <label class="flex flex-col gap-1">
            Code
            <input
              type="text"
              bind:value={code}
              class="text-xl text-black focus-within:ring-teal-700 rounded-lg w-full"
            />
            {#if error === 'game_not_found'}
              <div class="text-red-500 text-sm">Game not found</div>
            {/if}
          </label>
          <label class="flex flex-col gap-1">
            Name
            <input
              type="text"
              bind:value={name}
              class="text-xl text-black focus-within:ring-teal-700 rounded-lg w-full"
            />
            {#if error === 'invalid_name'}
              <div class="text-red-500 text-sm">Invalid name</div>
            {/if}
            {#if error === 'name_taken'}
              <div class="text-red-500 text-sm">Name already taken</div>
            {/if}
          </label>
          <button
            class="py-4 px-6 bg-teal-700 text-center rounded-lg text-lg disabled:opacity-50"
            disabled={code.length != 6 || name.length === 0}
          >
            Join
          </button>
          {#if error === 'game_already_started'}
            <div class="text-red-500 text-sm">Game already started</div>
          {:else if error && !['game_not_found', 'name_taken', 'invalid_name', 'game_already_started'].includes(error)}
            <div class="text-red-500 text-sm">An error occurred: {error}</div>
          {/if}
        </form>
      {/if}
    </div>
  </div>
</div>
