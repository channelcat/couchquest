<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import Button from "./components/form/Button.svelte";
  import Input from "./components/form/Input.svelte";
  import type { ActionRequest } from "./backend";
  import { showNotice } from "./components/Alert.svelte";
  import { shrinkY } from "./shared/transitions";

  let desiredActions: ActionRequest[] = [
    { action: "Take a drink", amount: 10, theme: "" },
  ];

  const dispatch = createEventDispatcher();
</script>

<div>
  <!-- Form to fill in drinks and finishes as int inputs with labels-->
  {#each desiredActions as action, i}
    <div class="relative" transition:shrinkY>
      <div class="absolute top-1 left-1">
        {#if i > 0}
          <Button
            on:click={() => {
              desiredActions.splice(i, 1);
              desiredActions = desiredActions;
            }}
            size="sm"
            style="secondary"
          >
            X
          </Button>
        {/if}
      </div>
      <div class="flex space-x-4 mt-4">
        <div class="text-sm flex text-right items-center justify-end w-32">
          Action:
        </div>
        <div class="flex space-x-2 items-center grow">
          <Input
            type="text"
            bind:value={action.action}
            placeholder="Do a thing"
          />
          <Input type="number" min={1} max={100} bind:value={action.amount} />
          <span class="text-sm">times</span>
        </div>
      </div>
      <div class="flex space-x-4 mt-2">
        <div class="text-sm flex text-right items-center justify-end w-32">
          Theme (optional):
        </div>
        <div class="grow">
          <Input bind:value={action.theme} maxlength={100} />
        </div>
      </div>
    </div>
  {/each}
  <div class="flex justify-center mt-4 flex-col space-y-10 items-center">
    <div>
      <Button
        on:click={() =>
          (desiredActions = [
            ...desiredActions,
            {
              action: "",
              amount: 1,
              theme: "",
            },
          ])}
        style="form"
        icon="Plus"
      >
        Add Action
      </Button>
    </div>
    <div>
      <Button
        size="xl"
        icon="Wrench"
        on:click={() => {
          for (const action of desiredActions) {
            if (!action.action.trim() || !action.amount) {
              showNotice("Please fill in all fields");
              return;
            }
          }
          dispatch("generate", {
            desiredActions,
          });
        }}
      >
        Generate
      </Button>
    </div>
  </div>
</div>
