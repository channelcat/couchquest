<script lang="ts">
  import type { GeneratedGames } from "./backend";

  export let results: GeneratedGames;
</script>

<h3 class="my-4 text-lg">Suggestions</h3>

{#each results.actions as action}
  <div class="border p-4 my-4 rounded mb-6 shadow-md w-3/4">
    <div class="flex justify-between items-center mb-4">
      <div class="w-8"></div>
      <div class="flex flex-col space-y-2">
        <h3 class="text-lg">{action.action}</h3>
        <div class="text-sm">
          ~{action.games} drinks
        </div>
      </div>
      <div class="text-sm w-8">Instruct</div>
    </div>
  </div>
{/each}
