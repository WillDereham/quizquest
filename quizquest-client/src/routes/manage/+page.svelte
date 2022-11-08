<script lang="ts">
  import { goto } from '$app/navigation'
  import { endGame, manager } from '$lib/manager'
  import { faDoorOpen } from '@fortawesome/free-solid-svg-icons'
  import PreGameLobby from './PreGameLobby.svelte'
  import { onMount } from 'svelte'
  import Fa from 'svelte-fa'

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
      <button on:click={endGame} class="p-6 hover:bg-violet-900 ml-auto">
        <Fa icon={faDoorOpen} />
      </button>
    </div>
    {#if $manager.status === 'waiting_for_start'}
      <PreGameLobby />
    {/if}
  </div>
{/if}
