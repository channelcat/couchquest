<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { type SearchResult } from "./backend";
  export let result: SearchResult;
</script>

{#if result.service === "youtube"}
  <div class="flex items-center justify-center">
    <iframe
      width="560"
      height="315"
      src="https://www.youtube.com/embed/{result.id}"
      title=""
      frameBorder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
      allowFullScreen
    ></iframe>
  </div>
{:else if result.image_url}
  <img
    class="mx-auto max-h-48 max-w-96"
    src={result.image_url}
    alt={result.title}
  />
{/if}
