<script lang="ts">
  import { faMedal } from '@fortawesome/free-solid-svg-icons'

  import Fa from 'svelte-fa'

  export let place: number
</script>

<div class="flex flex-col items-center gap-4">
  <div
    class="h-32 aspect-square rounded-full shadow-2xl flex items-center justify-center {place === 1
      ? 'bg-orange-400'
      : place === 2
      ? 'bg-[#c0c0c0]'
      : 'bg-amber-700'} "
  >
    <Fa icon={faMedal} class="text-5xl" />
  </div>
  <div class="text-2xl">
    {#if place === 1}
      1st
    {:else if place === 2}
      2nd
    {:else}
      3rd
    {/if}
  </div>
</div>
