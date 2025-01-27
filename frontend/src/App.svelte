<script lang="ts">
  import {
    mediaSearch,
    gameGenerate as generateRequest,
    type SearchResult as SearchResultType,
    type GeneratedGames,
  } from "./backend";

  import Logo from "./assets/couchquest-large.png";
  import Icon from "./assets/couchquest-icon.png";
  import Alert from "./components/Alert.svelte";
  import Button from "./components/form/Button.svelte";
  import Input from "./components/form/Input.svelte";
  import Loading from "./components/Loading.svelte";
  import Toast from "./components/Toast.svelte";
  import GeneratedResults from "./GeneratedResults.svelte";
  import Generator from "./GeneratorForm.svelte";
  import ResultSelector, {
    type SelectedResultType,
  } from "./ResultSelector.svelte";
  import SelectedResult from "./SelectedResult.svelte";
  import { apiCall } from "./shared/backend";
  import { shrinkY } from "./shared/transitions";

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

<svelte:head>
  <link rel="icon" type="image/x-icon" href={Icon} />
</svelte:head>

<Alert />
<Toast />
<Loading loading={generating || searching} />

<section class="flex flex-col p-4 items-center justify-center h-full w-full">
  <img
    src={Logo}
    alt="Logo"
    class="h-[min(20vh,20vw)] w-[min(20vh,20vw)] mb-6"
  />
  {#if !selected}
    <form
      class="flex justify-center w-full max-w-96 shadow-lg rounded-lg mb-10"
      on:submit|preventDefault={search}
    >
      <Input
        fill
        bind:value={query}
        placeholder="Search for a movie or TV show"
        left
      />
      <Button loading={searching} right>Search</Button>
    </form>
  {/if}

  {#if selected}
    <div transition:shrinkY>
      <SelectedResult {selected} on:deselect={() => (selected = null)} />
      {#if generatedResults}
        <GeneratedResults results={generatedResults} />
      {:else}
        <div transition:shrinkY>
          <Generator on:generate={generate} />
        </div>
      {/if}
    </div>
  {:else if searchResults}
    <div transition:shrinkY>
      <ResultSelector on:select={selectResult} results={searchResults} />
    </div>
  {/if}
</section>
