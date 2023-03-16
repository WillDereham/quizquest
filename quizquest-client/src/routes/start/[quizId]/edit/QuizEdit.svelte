<script lang="ts">
  import type { Quiz } from '$lib/quizzes'

  export let quiz: Quiz

  let title = quiz.title
  $: title = title.substring(0, 100)
  let description = quiz.description
  $: description = description.substring(0, 100)
  let default_time_limit = quiz.default_time_limit
</script>

<div class="flex flex-col items-center p-8 gap-6">
  <h1 class="text-4xl">Edit Quiz</h1>
  <form class="flex flex-col gap-4 max-w-md w-full">
    <label class="flex flex-col gap-1">
      Title
      <input
        type="text"
        bind:value={title}
        class="text-xl text-black focus-within:ring-teal-700 rounded-lg w-full"
      />
      <!-- {#if error === 'game_not_found'}
      <div class="text-red-500 text-sm">Game not found</div>
    {/if} -->
    </label>
    <label class="flex flex-col gap-1">
      Description
      <input
        type="text"
        bind:value={description}
        class="text-xl text-black focus-within:ring-teal-700 rounded-lg w-full"
      />
    </label>
    <div class="flex flex-col gap-1">
      Default time limit (seconds)
      <ul class="flex justify-evenly relative">
        {#each [5, 10, 15, 20, 30, 45, 60] as value}
          <li class="grow">
            <label class="flex flex-col items-center gap-1 p-2">
              <input
                type="radio"
                name="defaultTimeLimit"
                {value}
                bind:group={default_time_limit}
                class="text-pink-500 focus:ring-pink-500"
              />
              {value}
            </label>

            <!-- class="text-xl text-black focus-within:ring-teal-700 rounded-lg w-full" -->
          </li>
        {/each}
      </ul>
    </div>
  </form>
</div>
