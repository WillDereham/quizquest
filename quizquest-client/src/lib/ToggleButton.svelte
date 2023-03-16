<script lang="ts">
  import { faCheck, faXmark } from '@fortawesome/free-solid-svg-icons'
  import Fa from 'svelte-fa'

  export let checked = false
</script>

<!-- Modified version of https://www.hyperui.dev/components/application-ui/toggles#component-2 -->

<label class="flex items-center gap-4">
  <div class="grow">
    <slot />
  </div>
  <div class="relative h-8 w-14 cursor-pointer">
    <input type="checkbox" bind:checked class="peer sr-only" />

    <span
      class="{checked ? 'bg-pink-500' : 'bg-gray-300'} absolute inset-0 rounded-full transition"
    />

    <span
      class="{checked
        ? 'translate-x-6 text-pink-600'
        : 'text-gray-400'} absolute inset-0 m-1 inline-flex h-6 w-6 items-center justify-center rounded-full bg-white transition"
    >
      <Fa icon={faXmark} class="h-4 w-4 {checked ? 'hidden' : ''}" />
      <Fa icon={faCheck} class="h-4 w-4 {checked ? '' : 'hidden'}" />
    </span>
  </div>
</label>
