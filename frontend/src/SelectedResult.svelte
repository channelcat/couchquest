<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import type { SelectedResultType } from "./ResultSelector.svelte";
  import Button from "./components/form/Button.svelte";
  export let selected: SelectedResultType;
  const dispatch = createEventDispatcher();
</script>

<div class="border p-4 my-4 rounded mb-6 shadow-md w-3/4">
  <div class="flex justify-between items-center mb-4">
    <div class="w-8">
      <Button on:click={() => dispatch("deselect")} size="sm" style="danger"
        >X</Button
      >
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
  {#if selected.result.image_url}
    <img
      class="mx-auto"
      src={selected.result.image_url}
      alt={selected.result.title}
    />
  {/if}
</div>
