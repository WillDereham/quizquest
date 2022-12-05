<script lang="ts">
  import { gameResults, manager, nextQuestion, skipQuestion } from '$lib/manager'
  import { fly } from 'svelte/transition'
  import { onMount } from 'svelte'
  import { answerColourClasses } from '$lib/answerColours'
  import QuestionLeaderboard from './QuestionLeaderboard.svelte'

  $: question = $manager?.current_question
  $: lastQuestion = $manager?.question_results?.last_question ?? null

  let timerBar: HTMLDivElement
  onMount(() => {
    if (duration) {
      timerBar.animate([{ transform: 'translate(-100%)' }, { transform: 'translate(0)' }], {
        duration: duration * 1000,
        easing: 'linear',
      })
    }
  })

  let showLeaderboard = false

  export let duration: number | null
  export let showAnswers: boolean = false
  export let questionResults: boolean = false
</script>

{#if question}
  <div class="w-full h-6 relative overflow-hidden {duration ? 'bg-white bg-opacity-10' : ''}">
    {#if duration}
      <div
        bind:this={timerBar}
        class="absolute top-0 left-0 w-[calc(100%+.75rem)] -translate-x-full bg-pink-500 bottom-0 rounded-r-full"
      />
    {/if}
  </div>
  <div
    class="grid grid-cols-1 h-full {showAnswers && !showLeaderboard
      ? 'grid-rows-[auto,1fr]'
      : 'grid-rows-1'} relative"
  >
    {#if showAnswers && !questionResults}
      <button
        class="bg-pink-500 rounded-md py-2 px-4 absolute right-10 top-4"
        on:click={skipQuestion}
      >
        Skip
      </button>
    {:else if questionResults}
      <button
        class="bg-pink-500 rounded-md py-2 px-4 absolute right-10 top-4"
        on:click={showLeaderboard
          ? lastQuestion
            ? gameResults
            : nextQuestion
          : () => (showLeaderboard = true)}
      >
        Next
      </button>
    {/if}
    {#if showLeaderboard}
      <div class="flex flex-col justify-center h-full">
        <QuestionLeaderboard />
      </div>
    {:else}
      <div class="flex {showAnswers ? 'items-start' : 'items-center'} justify-center p-4">
        <div class="flex flex-col items-center gap-6 p-4 grow">
          <h2 class="text-2xl">Question #{question.number}</h2>
          <h1 class="text-7xl font-medium break-words max-w-[100vw] text-center leading-relaxed">
            {question.text}
          </h1>
        </div>
      </div>
      {#if showAnswers}
        <div
          class="grid grid-cols-2 auto-rows-fr gap-2 p-2"
          in:fly={{ y: 200, duration: questionResults ? 0 : 1000, opacity: 100 }}
        >
          {#each question.answers as answer, index (answer.id)}
            <div
              class="flex flex-col items-center rounded-md shadow-xl p-4
              {questionResults
                ? answer.correct
                  ? 'bg-green-500'
                  : 'bg-red-500'
                : answerColourClasses[index % answerColourClasses.length]}
              {question.answers.length % 2 == 1 ? 'last:col-span-2' : ''}"
            >
              <div class="text-xl">{'ABCDEF'[index]}</div>
              <div class="break-words max-w-full text-2xl flex items-center justify-center grow">
                {answer.text}
              </div>
            </div>
          {/each}
        </div>
      {/if}
    {/if}
  </div>
{:else}
  Error: current_question not set
{/if}
