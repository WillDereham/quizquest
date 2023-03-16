<script lang="ts">
  import QuizEdit from './QuizEdit.svelte'
  import type { PageData } from './$types'

  export let data: PageData

  $: quiz = data.quiz
</script>

{#if quiz !== null}
  <QuizEdit {quiz} />
  <div>{JSON.stringify(data.quiz)}</div>
{:else}
  <div>Not found</div>
{/if}
