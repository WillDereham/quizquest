<script lang="ts">
  import { endGame, manager } from '$lib/manager'
  import ResultsMedal from '$lib/ResultsMedal.svelte'

  $: leaderboard = $manager?.game_results?.leaderboard
</script>

{#if leaderboard}
  <div class="flex h-full w-full relative">
    <button class="bg-pink-500 rounded-md py-2 px-4 absolute right-10 top-10" on:click={endGame}>
      Menu
    </button>
    <div class="grow flex flex-col justify-end">
      {#if leaderboard[1]}
        <div class="h-1/4 flex flex-col items-center justify-center gap-2">
          <div class="text-5xl">
            {leaderboard[1].name}
          </div>
          <div>{leaderboard[1].score} points</div>
        </div>
      {/if}
      <div class="h-1/2 bg-pink-500 pt-6">
        <ResultsMedal place={2} />
      </div>
    </div>
    <div class="grow flex flex-col justify-end">
      {#if leaderboard[0]}
        <div class="h-1/4 flex flex-col items-center justify-center gap-2">
          <div class="text-5xl">
            {leaderboard[0].name}
          </div>
          <div>{leaderboard[0].score} points</div>
        </div>
      {/if}
      <div class="h-3/4 bg-pink-500 pt-6">
        <ResultsMedal place={1} />
      </div>
    </div>
    <div class="grow flex flex-col justify-end">
      {#if leaderboard[2]}
        <div class="h-1/4 flex flex-col items-center justify-center gap-2">
          <div class="text-5xl">
            {leaderboard[2].name}
          </div>
          <div>{leaderboard[2].score} points</div>
        </div>
      {/if}
      <div class="h-1/3 bg-pink-500 pt-6">
        <ResultsMedal place={3} />
      </div>
    </div>
  </div>
{:else}
  Error: leaderboard not set
{/if}
