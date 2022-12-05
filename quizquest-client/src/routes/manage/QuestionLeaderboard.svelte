<script lang="ts">
  import { manager } from '$lib/manager'

  $: leaderboard = $manager?.question_results?.leaderboard ?? null
</script>

{#if leaderboard}
  <div class="p-4 text-xl">
    <h1 class="text-center text-4xl mb-4">Leaderboard</h1>
    <ul class="flex flex-col gap-2">
      <li class="flex p-3">
        <div class="w-24">Position</div>
        <div class="grow">Name</div>
        <div class="w-40">Score</div>
      </li>
      {#each leaderboard as player, index (player.id)}
        <li class="flex p-3 bg-violet-500 rounded-lg">
          <div class="w-24">{index + 1}</div>
          <div class="grow">{player.name}</div>
          <div class="w-40">{player.score}</div>
        </li>
      {/each}
    </ul>
  </div>
{:else}
  Error: leaderboard not set
{/if}
