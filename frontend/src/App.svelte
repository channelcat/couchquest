<script lang="ts">
  import {
    mediaSearch,
    generate as generateRequest,
    type SearchResult as SearchResultType,
    type GeneratedGames,
  } from "./backend";

  import Alert from "./components/Alert.svelte";
  import Button from "./components/form/Button.svelte";
  import Input from "./components/form/Input.svelte";
  import Loading from "./components/Loading.svelte";
  import Toast from "./components/Toast.svelte";
  import GeneratedResults from "./GeneratedResults.svelte";
  import Generator from "./Generator.svelte";
  import ResultSelector, {
    type SelectedResultType,
  } from "./ResultSelector.svelte";
  import SelectedResult from "./SelectedResult.svelte";
  import { apiCall } from "./shared/backend";

  let query = "";
  let generating = false;
  let searching = false;
  let searchResults: SearchResultType[] | null = null;
  let selected: SelectedResultType | null = null;
  let generatedResults: GeneratedGames = null;

  async function search() {
    searching = true;
    selected = null;
    searchResults = null;

    const [results] = await apiCall(mediaSearch, { query });
    if (results) {
      searchResults = results;
    }

    searching = false;
  }

  async function generate(e: CustomEvent<any>) {
    const { desiredActions } = e.detail;

    generating = true;
    generatedResults = null;

    const [results] = await apiCall(generateRequest, {
      requestBody: {
        id: selected.episode?.id || selected.result.id,
        imdb_id: selected.episode?.imdb_id || selected.result.imdb_id,
        parent_imdb_id: selected.episode ? selected.result.imdb_id : null,
        service: selected.result.service,
        desired_actions: desiredActions,
      },
    });
    if (results) {
      generatedResults = results;
    }

    generating = false;
  }

  function selectResult(e: CustomEvent<SelectedResultType>) {
    selected = e.detail;
    generatedResults = null;
  }
</script>

<Alert />
<Toast />

<section class="flex flex-col p-4 items-center justify-center h-full w-full">
  {#if !selected}
    <form
      class="flex space-x-2 justify-center px-4 w-full"
      on:submit|preventDefault={search}
    >
      <Input
        fill
        bind:value={query}
        placeholder="Search for a movie or TV show"
      />
      <Button loading={searching}>Search</Button>
    </form>
  {/if}

  {#if selected}
    <SelectedResult {selected} on:deselect={() => (selected = null)} />
    {#if generating || generatedResults}
      <Loading loading={generating}>
        <GeneratedResults results={generatedResults} />
      </Loading>
    {:else}
      <Generator on:generate={generate} />
    {/if}
  {:else}
    <Loading loading={searching}>
      {#if searchResults}
        <ResultSelector on:select={selectResult} results={searchResults} />
      {/if}
    </Loading>
  {/if}
</section>
