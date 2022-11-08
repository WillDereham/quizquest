<script lang="ts">
  import { goto } from '$app/navigation'
  import { startGame } from '$lib/manager'
  import { onMount } from 'svelte'

  let loading = false
  let error: string | null = null

  onMount(async () => {
    loading = true
    error = null
    try {
      await startGame().catch(async (e: string) => {
        error = e
      })
      goto('/manage')
    } finally {
      loading = false
    }
  })
</script>

<div>Start</div>
