<script lang="ts">
  import { onMount } from 'svelte'
  import Fa from 'svelte-fa'
  import { faDoorOpen, faLink, faUser } from '@fortawesome/free-solid-svg-icons'
  import { player, leaveGame } from '$lib/player'
  import { goto } from '$app/navigation'
  import WaitingForStart from './WaitingForStart.svelte'
  import { getJoinUrl } from '$lib/url'

  onMount(async () => {
    if ($player === null) {
      goto('/join')
    }
  })

  let linkCopied = false

  async function copyLink(): Promise<void> {
    await navigator.clipboard.writeText(getJoinUrl($player!.code))

    linkCopied = true
    setTimeout(() => {
      linkCopied = false
    }, 1000)
  }
</script>

{#if $player !== null}
  <div class="h-full flex flex-col">
    <div class="flex bg-violet-800 h-20">
      <div class="p-6 font-medium text-lg">QuizQuest</div>
      <button class="flex items-center gap-3 p-6 hover:bg-violet-900 relative" on:click={copyLink}>
        <Fa icon={faLink} />
        <div class="font-mono">
          {$player.code}
        </div>
        <div
          class="absolute top-full left-1/2 mt-2 w-max -translate-x-1/2 rounded-md bg-cyan-400 text-gray-900 py-1 px-2  transition-[opacity,visibility] {linkCopied
            ? 'visible opacity-100'
            : 'invisible opacity-0'}"
        >
          Link Copied
        </div>
      </button>
      <div class="flex items-center gap-3 p-6"><Fa icon={faUser} />{$player.name}</div>

      <button on:click={leaveGame} class="p-6 hover:bg-violet-900 ml-auto">
        <Fa icon={faDoorOpen} />
      </button>
    </div>
    {#if $player.status === 'waiting_for_start'}
      <WaitingForStart />
    {/if}
  </div>
{/if}
