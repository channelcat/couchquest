<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import type { SelectedResultType } from "./ResultSelector.svelte";
  import Button from "./components/form/Button.svelte";
  import ResultMedia from "./ResultMedia.svelte";
  import Card from "./components/Card.svelte";
  export let selected: SelectedResultType;
  const dispatch = createEventDispatcher();
</script>

<Card>
  <div class="flex justify-between mb-4">
    <div class="w-8">
      <Button on:click={() => dispatch("deselect")} size="sm" style="danger">
        X
      </Button>
    </div>
    <div class="flex flex-col space-y-2">
      <h3 class="text-lg">{selected.result.title}</h3>

      {#if selected.season}
        <span class="text-sm">
          Season {selected.season.number}
        </span>
      {/if}
      {#if selected.episode}
        <span class="text-sm">
          E{selected.episode.number} - {selected.episode.title}
        </span>
      {/if}
    </div>
    <div class="text-sm w-8">
      {selected.result.release_year}
    </div>
  </div>
  <ResultMedia result={selected.result} />
</Card>
