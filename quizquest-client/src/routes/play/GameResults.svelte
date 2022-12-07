<script lang="ts">
  import { leaveGame, player } from '$lib/player'
  import ResultsMedal from '$lib/ResultsMedal.svelte'

  $: rank = $player?.rank ?? null
  $: score = $player?.score ?? 0

  function getSuffix(num: number) {
    const lastDigit = num % 10
    const tensDigit = Math.trunc((num % 100) / 10)

    if (tensDigit === 1 || lastDigit > 3 || lastDigit === 0) return 'th'
    if (lastDigit === 1) return 'st'
    if (lastDigit === 2) return 'nd'
    if (lastDigit === 3) return 'rd'
  }
</script>

{#if $player !== null && rank !== null}
  <div class="flex flex-col items-center justify-center h-full gap-4 relative">
    <button class="bg-pink-500 rounded-md py-2 px-4 absolute right-10 top-10" on:click={leaveGame}>
      Menu
    </button>
    {#if rank < 4}
      <ResultsMedal place={rank} />
    {:else}
      <div class="text-4xl">{rank}{getSuffix(rank)}</div>
    {/if}
    <div class="text-xl">{score} points</div>
  </div>
{:else}
  Error: rank or score not set
{/if}
