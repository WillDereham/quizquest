<script lang="ts">
  import { manager } from '$lib/manager'
  import { fly } from 'svelte/transition'
  import { onMount } from 'svelte'

  $: question = $manager?.current_question

  let timerStarted = false
  onMount(() => {
    setTimeout(() => {
      timerStarted = true
    }, 10)
  })

  export let duration: number | null
  export let showAnswers: boolean = false
  export let showCorrect: boolean = false

  const colourClasses = [
    'bg-fuchsia-500',
    'bg-yellow-500',
    'bg-cyan-500',
    'bg-emerald-500',
    'bg-orange-500',
    'bg-violet-500',
  ]
</script>

{#if question}
  <div class="w-full h-6  relative overflow-hidden {duration ? 'bg-white bg-opacity-10' : ''}">
    {#if duration}
      <div
        class="absolute top-0 left-0 w-full -translate-x-full bg-pink-500 bottom-0 transition-transform ease-linear rounded-r-full"
        style:transform="translate({timerStarted ? 0 : '-100%'})"
        style:transition-duration="{duration * 1000}ms"
      />
    {/if}
  </div>
  <!-- <progress
    value=".5"
    class="accent-pink-500 [&::-moz-progress-bar]:bg-pink-500 [&::-webkit-progress-value]:bg-pink-500 bg-transparent"
  /> -->
  <div class="grid grid-cols-1 h-full {showAnswers ? 'grid-rows-[auto,1fr]' : 'grid-rows-1'}">
    <div class="flex flex-col items-center justify-center">
      <div class="flex flex-col items-center gap-6 p-4">
        <h2 class="text-2xl">Question #{question.number}</h2>
        <h1 class="text-7xl font-medium break-words max-w-[100vw] text-center leading-relaxed">
          {question.text}
        </h1>
      </div>
    </div>
    {#if showAnswers}
      <div
        class="grid grid-cols-2 auto-rows-fr gap-2 p-2"
        in:fly={{ y: 200, duration: showCorrect ? 0 : 1000, opacity: 100 }}
      >
        {#each question.answers as answer, index (answer.id)}
          <div
            class="flex items-center justify-center rounded-md shadow-xl p-4
              {showCorrect
              ? answer.correct
                ? 'bg-green-500'
                : 'bg-red-500'
              : colourClasses[index % colourClasses.length]}
              {question.answers.length % 2 == 1 ? 'last:col-span-2' : ''}"
          >
            <div class="break-words max-w-full text-2xl">
              {answer.text}
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </div>
{:else}
  Error: current_question not set
{/if}
