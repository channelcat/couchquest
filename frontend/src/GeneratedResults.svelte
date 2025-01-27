<script lang="ts">
  import type { GeneratedGames } from "./backend";
  import Card from "./components/Card.svelte";
  import Tab from "./components/Tab.svelte";
  import TabGroup from "./components/TabGroup.svelte";

  export let results: GeneratedGames;
</script>

<Card>
  <h3 class="mb-4 text-sm text-gray-600 mb-8">
    {results.explanation}
  </h3>

  <TabGroup id="games" history={false} save={false} style="card">
    {#each results.actions as action}
      <Tab name={action.action}>
        <div>
          <ul class="gap-2 divide-y space-y-3">
            {#each action.games as game}
              <li class="pt-3 flex flex-col space-y-2">
                <h3 class="text-lg">{game.name}</h3>
                <div class="text-sm">
                  Estimate: ~{game.estimated_amount}
                  time{game.estimated_amount > 1 ? "s" : ""}
                </div>
                <div class="text-sm text-gray-600">
                  {game.instructions}
                </div>
              </li>
            {/each}
          </ul>
        </div>
      </Tab>
    {/each}
    {#if results.suggestions?.length}
      <Tab name="Suggestions">
        <div>
          <ul class="gap-2 divide-y space-y-3">
            {#each results.suggestions as suggestion}
              <li class="pt-3 flex flex-col space-y-2">
                <div class="text-sm">
                  Estimate: ~{suggestion.estimated_amount}
                  time{suggestion.estimated_amount > 1 ? "s" : ""}
                </div>
                <div class="text-sm text-gray-600">
                  {suggestion.suggestion}
                </div>
              </li>
            {/each}
          </ul>
        </div>
      </Tab>
    {/if}
  </TabGroup>
</Card>
