<script lang="ts">
  import { goto } from '$app/navigation'
  import { startGame } from '$lib/manager'
  import type { PageData } from './$types'
  import BackArrow from '$lib/BackArrow.svelte'
  import ToggleButton from '$lib/ToggleButton.svelte'

  let loading = false
  let error: string | null = null

  let randomiseQuestionOrder = false
  let randomiseAnswerOrder = true

  export let data: PageData

  async function start() {
    loading = true
    error = null
    try {
      await startGame({ quizId: data.quiz.id, randomiseQuestionOrder, randomiseAnswerOrder }).catch(
        async (e: string) => {
          error = e
        },
      )
      goto('/manage')
    } finally {
      loading = false
    }
  }
</script>

{#if loading}
  <div>Loading...</div>
{:else}
  <div class="flex flex-col">
    <div class="flex">
      <BackArrow href="/start" />
    </div>
    <div class="flex flex-col items-center p-8 gap-6">
      <h1 class="text-4xl">{data.quiz.title}</h1>
      <form on:submit={start} class="flex flex-col gap-4">
        <ToggleButton bind:checked={randomiseQuestionOrder}>Randomise Question Order</ToggleButton>
        <ToggleButton bind:checked={randomiseAnswerOrder}>Randomise Answer Order</ToggleButton>
        <button
          class="py-4 px-6 bg-pink-500 text-center rounded-lg text-lg disabled:opacity-50 self-center"
          type="submit"
        >
          Start Game
        </button>
      </form>
    </div>
  </div>
{/if}
