<script lang="ts">
  import { player } from '$lib/player'

  $: question = $player?.current_question
</script>

{#if question}
  <div class="flex flex-col gap-4 text-center items-center justify-center h-full">
    <div class="text-4xl">Question #{question.number}</div>
    <div class="text-xl">Get ready to answer!</div>
  </div>
{:else}
  Error: current_question not set
{/if}
