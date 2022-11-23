<script lang="ts">
  import { answerColourClasses } from '$lib/answerColours'
  import { answerQuestion, player } from '$lib/player'

  $: question = $player?.current_question
</script>

{#if question}
  <div class="grid grid-cols-2 auto-rows-fr gap-2 p-2 h-full">
    {#each question.answers as answer, index (answer.id)}
      <button
        class="flex items-center justify-center rounded-md shadow-xl p-4
              {answerColourClasses[index % answerColourClasses.length]}
              {question.answers.length % 2 == 1 ? 'last:col-span-2' : ''}"
        on:click={() => answerQuestion(answer.id)}
      >
        <div class="text-4xl">
          {'ABCDEF'[index]}
        </div>
      </button>
    {/each}
  </div>
{:else}
  Error: current_question not set
{/if}
