<script lang="ts">
  import { page } from '$app/stores'
  import { beginGame, kickPlayer, manager, type ManagerPlayer } from '$lib/manager'
  import { getQRCodeURL } from '$lib/url'
  import { faPlay, faXmark } from '@fortawesome/free-solid-svg-icons'
  import { onMount } from 'svelte'
  import Fa from 'svelte-fa'

  let qrCodeURL: string | null = null

  let players: ManagerPlayer[]
  $: players = [...$manager!.players.values()].reverse()

  onMount(async () => {
    qrCodeURL = await getQRCodeURL($manager!.code)
  })
</script>

{#if $manager !== null}
  <div
    class="grid grid-cols-1 md:grid-cols-[1fr,auto] grid-rows-[auto,1fr] max-h-[calc(100vh-5rem)]"
  >
    <div class="row-start-1 col-start-1 p-8 gap-2 flex flex-col">
      <div class="text-xl">
        Go to <span class="font-mono">{$page.url.host}/join</span>
      </div>
      <div class="text-xl">Enter this code:</div>
      <div class="font-mono text-8xl ">
        {$manager.code}
      </div>
    </div>
    <div class="row-start-2 col-start-1 overflow-y-scroll p-8 flex flex-col gap-4">
      <div class="flex items-center">
        <p class="text-xl">{players.length} player{players.length != 1 ? 's' : ''} joined</p>
        <button
          class="bg-pink-500 py-2 px-4 flex rounded-md items-center gap-2 self-center ml-auto"
          class:opacity-50={players.length === 0}
          disabled={players.length === 0}
          on:click={(e) => beginGame()}
        >
          <Fa icon={faPlay} />
          Start
        </button>
      </div>
      <ul class="flex flex-wrap gap-2">
        {#each players as player}
          <li>
            <button
              class="bg-cyan-500 py-2 px-4 flex rounded-md items-center gap-2 group"
              on:click={(e) => kickPlayer(player.id)}
            >
              {player.name}
              <Fa icon={faXmark} class="opacity-50 group-hover:opacity-100" />
            </button>
          </li>
        {/each}
      </ul>
    </div>

    <div class="hidden md:flex row-start-1 row-span-2 col-start-2 p-8 flex-col gap-4">
      <div class="text-center text-xl">Scan QR code to join</div>
      {#if qrCodeURL}
        <img
          src={qrCodeURL}
          alt="QR code to join game"
          class=" aspect-square "
          style="image-rendering: pixelated;"
        />
      {/if}
    </div>
  </div>
{/if}
