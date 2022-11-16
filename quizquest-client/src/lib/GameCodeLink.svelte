<script lang="ts">
  import { getJoinUrl } from '$lib/url'
  import { faLink } from '@fortawesome/free-solid-svg-icons'
  import Fa from 'svelte-fa'

  export let code: string

  let linkCopied = false

  async function copyLink(): Promise<void> {
    await navigator.clipboard.writeText(getJoinUrl(code))

    linkCopied = true
    setTimeout(() => {
      linkCopied = false
    }, 1000)
  }
</script>

<button class="flex items-center gap-3 p-6 hover:bg-violet-900 relative" on:click={copyLink}>
  <Fa icon={faLink} />
  <div class="font-mono">
    {code}
  </div>
  <div
    class="absolute top-full left-1/2 mt-2 w-max -translate-x-1/2 rounded-md bg-cyan-400 text-gray-900 py-1 px-2  transition-[opacity,visibility] {linkCopied
      ? 'visible opacity-100'
      : 'invisible opacity-0'}"
  >
    Link Copied
  </div>
</button>
