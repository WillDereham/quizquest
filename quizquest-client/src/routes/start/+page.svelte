<script lang="ts">
  import { goto } from '$app/navigation'
  import { startGame } from '$lib/manager'
  import type { PageData } from './$types'
  import { onMount } from 'svelte'
  import Fa from 'svelte-fa'
  import { faPen, faPlay } from '@fortawesome/free-solid-svg-icons'

  let loading = false
  let error: string | null = null

  export let data: PageData

  async function start(quizId: string) {
    loading = true
    error = null
    try {
      await startGame(quizId).catch(async (e: string) => {
        error = e
      })
      goto('/manage')
    } finally {
      loading = false
    }
  }

  function formatRelativeDate(timestamp: number) {
    const now = new Date().getTime() / 1000
    const seconds = Math.floor(now - timestamp)
    if (seconds < 60) return `${seconds} second${seconds === 1 ? '' : 's'}`
    const minutes = Math.floor(seconds / 60)
    if (minutes < 60) return `${minutes} minute${minutes === 1 ? '' : 's'}`
    const hours = Math.floor(minutes / 60)
    if (hours < 24) return `${hours} hour${hours === 1 ? '' : 's'}`
    const days = Math.floor(hours / 24)
    return `${days} day${days === 1 ? '' : 's'}`
  }
</script>

{#if loading}
  <div>Loading...</div>
{:else}
  <div class="flex flex-col items-center p-8 gap-6">
    <h1 class="text-4xl">Start Game</h1>
    <ul class="flex flex-col gap-4">
      {#each data.quizzes as quiz}
        <li class="flex p-4 bg-violet-500 rounded-lg gap-4">
          <div class="flex flex-col grow">
            <h2 class="text-xl break-words">{quiz.title}</h2>
            <div class="">
              <p>
                <span class="break-words">{quiz.description}</span>
                -
                {quiz.questions.length} question{quiz.questions.length === 1 ? '' : 's'}
                - Last updated {formatRelativeDate(quiz.last_updated.seconds)} ago
              </p>
            </div>
          </div>
          <div class="flex items-center text-lg gap-2">
            <button
              class="flex items-center justify-center h-10 w-10 bg-violet-700 bg-opacity-30 hover:bg-opacity-50 rounded-lg"
              on:click={() => start(quiz.id)}
            >
              <Fa icon={faPlay} />
            </button>
            <button
              class="flex items-center justify-center h-10 w-10 bg-violet-700 bg-opacity-30 hover:bg-opacity-50 rounded-lg"
            >
              <Fa icon={faPen} />
            </button>
          </div>
        </li>
      {/each}
    </ul>
  </div>
{/if}
