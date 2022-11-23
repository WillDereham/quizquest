<script lang="ts">
  import { onMount } from 'svelte'
  import Fa from 'svelte-fa'
  import { faDoorOpen, faLink, faUser } from '@fortawesome/free-solid-svg-icons'
  import { player, leaveGame } from '$lib/player'
  import { goto } from '$app/navigation'
  import WaitingForStart from './WaitingForStart.svelte'
  import GameCodeLink from '$lib/GameCodeLink.svelte'
  import ShowQuestion from './ShowQuestion.svelte'
  import CollectAnswer from './CollectAnswer.svelte'
  import QuestionAnswered from './QuestionAnswered.svelte'
  import QuestionResults from './QuestionResults.svelte'

  onMount(async () => {
    if ($player === null) {
      goto('/join')
    }
  })
</script>

{#if $player !== null}
  <div class="h-full flex flex-col">
    <div class="flex bg-violet-800 h-20">
      <div class="p-6 font-medium text-lg">QuizQuest</div>
      <GameCodeLink code={$player.code} />
      <div class="flex items-center gap-3 p-6"><Fa icon={faUser} />{$player.name}</div>

      <button on:click={leaveGame} class="p-6 hover:bg-violet-900 ml-auto">
        <Fa icon={faDoorOpen} />
      </button>
    </div>
    {#if $player.status === 'waiting_for_start'}
      <WaitingForStart />
    {:else if $player.status === 'show_question'}
      <ShowQuestion />
    {:else if $player.status === 'collect_answers'}
      <CollectAnswer />
    {:else if $player.status === 'question_answered'}
      <QuestionAnswered />
    {:else if $player.status === 'question_results'}
      <QuestionResults />
    {:else}
      Unknown game status
    {/if}
  </div>
{/if}
