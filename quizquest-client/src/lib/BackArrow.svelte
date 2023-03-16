<script lang="ts">
  import { faArrowLeft } from '@fortawesome/free-solid-svg-icons'
  import Fa from 'svelte-fa'

  export let href: string
</script>

<a {href} class="p-6"><Fa icon={faArrowLeft} size="lg" /></a>
