<script lang="ts">
  import { goto } from '$app/navigation'
  import { endGame, manager } from '$lib/manager'
  import { faDoorOpen } from '@fortawesome/free-solid-svg-icons'
  import PreGameLobby from './PreGameLobby.svelte'
  import { onMount } from 'svelte'
  import Fa from 'svelte-fa'
  import ShowQuestion from './ShowQuestion.svelte'
  import GameCodeLink from '$lib/GameCodeLink.svelte'

  onMount(async () => {
    if ($manager === null) {
      goto('/')
    }
  })
</script>

{#if $manager !== null}
  <div class="flex flex-col h-screen max-h-full ">
    <div class="flex bg-violet-800 gap-6 h-20">
      <div class="p-6 font-medium text-lg">QuizQuest</div>
      <GameCodeLink code={$manager.code} />
      <button on:click={endGame} class="p-6 hover:bg-violet-900 ml-auto">
        <Fa icon={faDoorOpen} />
      </button>
    </div>
    {#if $manager.status === 'waiting_for_start'}
      <PreGameLobby />
    {:else if $manager.status === 'show_question'}
      <ShowQuestion duration={5} />
    {:else if $manager.status === 'collect_answers'}
      <ShowQuestion showAnswers={true} duration={$manager.current_question?.time_limit || null} />
    {:else if $manager.status === 'question_results'}
      <ShowQuestion showAnswers={true} showCorrect={true} duration={null} />
    {:else}
      Unknown game status
    {/if}
  </div>
{/if}
