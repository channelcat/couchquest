<script lang="ts" context="module">
  export type SelectedResultType = {
    result: SearchResult;
    season: Season | null;
    episode: Episode | null;
  };
</script>

<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { type Episode, type SearchResult, type Season } from "./backend";
  import Button from "./components/form/Button.svelte";
  import Select from "./components/form/Select.svelte";
  import ResultMedia from "./ResultMedia.svelte";
  import Card from "./components/Card.svelte";

  export let results: SearchResult[];

  let selectedSeasons: Record<string, Season> = {};
  let selectedEpisodes: Record<string, Episode> = {};
  const dispatch = createEventDispatcher();
</script>

{#if results.length}
  {#each results as result}
    <Card>
      <div class="flex justify-between items-center mb-4">
        <div class="w-4"></div>
        <h3 class="text-lg">{result.title}</h3>
        <div class="text-sm w-8">
          {result.release_year}
        </div>
      </div>
      <ResultMedia {result} />
      <div class="flex my-4 space-x-2 items-center justify-center">
        {#if result.seasons?.length}
          <Select
            options={[
              [undefined, "Select Season"],
              ...result.seasons
                .filter((s) => s.episodes.length)
                .map((s) => [s, `Season ${s.number}`]),
            ]}
            selected={selectedSeasons[result.id]}
            on:change={(e) => {
              selectedSeasons[result.id] = e.detail;
              selectedSeasons = selectedSeasons;
            }}
          />
          {#if selectedSeasons[result.id]}
            <Select
              options={[
                [undefined, "Select Episode"],
                ...selectedSeasons[result.id].episodes
                  .filter((e) => e.id)
                  .map((e) => [e, `E${e.number} - ${e.title}`]),
              ]}
              selected={selectedEpisodes[result.id]}
              on:change={(e) => {
                selectedEpisodes[result.id] = e.detail;
                selectedEpisodes = selectedEpisodes;
              }}
            />
          {/if}
        {/if}
        <Button
          on:click={() =>
            dispatch("select", {
              result,
              season: selectedSeasons[result.id],
              episode: selectedEpisodes[result.id],
            })}
          disabled={result.type === "series" && !selectedEpisodes[result.id]}
        >
          Select
        </Button>
      </div>
    </Card>
  {/each}
{:else}
  <div class="flex justify-center items-center mt-4">
    <div class="text-gray-600 text-sm">No results found</div>
  </div>
{/if}
