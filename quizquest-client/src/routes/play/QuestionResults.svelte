<script lang="ts">
  import { player } from '$lib/player'
  import { faCheck, faXmark } from '@fortawesome/free-solid-svg-icons'
  import Fa from 'svelte-fa'

  $: results = $player?.question_results
</script>

{#if results}
  <div class="flex flex-col gap-4 text-center items-center justify-center h-full ">
    <div
      class="rounded-full p-8 text-center aspect-square flex items-center justify-center {results.correct
        ? 'bg-green-500'
        : 'bg-red-500'}"
    >
      <Fa icon={results.correct ? faCheck : faXmark} class="text-8xl" />
    </div>
    <div class="text-6xl">{results.correct ? 'Correct' : 'Incorrect'}</div>
    <div class="text-4xl">{results.correct ? '+' : ''}{results.score_gained} points</div>
  </div>
{:else}
  Error: results not set
{/if}
