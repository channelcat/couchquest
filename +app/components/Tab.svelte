<script lang="ts">
  import { onDestroy, getContext, onMount } from "svelte";
  import type { IconType } from "./Icon.svelte";

  export let name: string;
  export let id: string = name;
  export let icon: IconType = undefined;

  const { register, deregister, currentTab } = getContext<any>("tabs");

  onMount(() => {
    register({ id, name, icon });
  });
  onDestroy(() => {
    deregister(id);
  });
</script>

{#if $currentTab === id}
  <slot />
{/if}
