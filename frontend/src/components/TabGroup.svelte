<script lang="ts">
  import { createEventDispatcher, setContext } from "svelte";
  import { writable } from "svelte/store";
  import type { IconType } from "./Icon.svelte";
  import Icon from "./Icon.svelte";

  export let id: string | undefined = undefined;
  export let centered = false;
  export let save = true;
  export let history = true;
  export let style: "card" | "default" = "default";

  const dispatcher = createEventDispatcher();

  type Tab = {
    name: string;
    id: string;
    icon?: IconType;
  };

  let tabs: Tab[] = [];
  let currentTab = writable(
    (id && history && window.location.hash.substring(1)) ||
      (id && save && localStorage[`tab-${id}`]) ||
      tabs[0]?.id ||
      undefined,
  );
  export let tabId = undefined;
  $: tabId = $currentTab;
  function register(tab: Tab) {
    tabs = [...tabs, tab];
    if ($currentTab === undefined) {
      setTab(tab.id);
    }
  }
  function deregister(tabId: string) {
    tabs.forEach((tab, index) => {
      if (tab.id === tabId) {
        tabs.splice(index, 1);
        tabs = tabs;
      }
    });
  }
  export function setTab(tabId: string) {
    const previousTabId = $currentTab;
    $currentTab = tabId;
    if (id && save) {
      localStorage[`tab-${id}`] = tabId;
    }
    if (id && history) {
      window.history.replaceState({}, undefined, `#${tabId}`);
    }
    dispatcher("select", { value: tabId, oldValue: previousTabId });
  }

  setContext("tabs", { register, deregister, currentTab });
</script>

<div class:mb-4={style === "default"}>
  <div class="hidden">
    <label for="tabs" class="sr-only">Select a tab</label>
    <!-- Use an "onChange" listener to redirect the user to the selected tab URL. -->
    <select
      id="tabs"
      name="tabs"
      class="block w-full rounded-md border-gray-300 focus:border-primary-500 focus:ring-primary-500 p-3"
    >
      {#each tabs as tab (tab.id)}
        <option value={tab.id}>{tab.name}</option>
      {/each}
    </select>
  </div>
  <div class="overflow-x-auto whitespace-nowrap sm:overflow-visible">
    <div
      class:border-b={style === "default"}
      class:border-gray-200={style === "default"}
    >
      <nav
        class:space-x-8={style === "default"}
        class="-mb-px flex"
        class:justify-center={centered}
        aria-label="Tabs"
      >
        {#each tabs as tab}
          <a
            href="{window.location.pathname}#{tab.id}"
            on:click|preventDefault|stopPropagation={() => setTab(tab.id)}
            class:border-primary-500={style === "default" &&
              tab.id === $currentTab}
            class:text-primary-600={style === "default" &&
              tab.id === $currentTab}
            class:border-transparent={style === "default" &&
              tab.id !== $currentTab}
            class:text-gray-500={style === "default" && tab.id !== $currentTab}
            class:hover:text-gray-700={style === "default" &&
              tab.id !== $currentTab}
            class:hover:border-gray-300={style === "default" &&
              tab.id !== $currentTab}
            class:border-b-2={style === "default"}
            class:py-4={style === "default"}
            class:px-1={style === "default"}
            class:border-b-white={style === "card" && tab.id === $currentTab}
            class:text-gray-400={style === "card" && tab.id !== $currentTab}
            class:bg-white={style === "card" && tab.id === $currentTab}
            class:mr-0.5={style === "card"}
            class:bg-gray-100={style === "card" && tab.id !== $currentTab}
            class:py-2={style === "card"}
            class:px-3={style === "card" && tab.id !== $currentTab}
            class:px-4={style === "card" && tab.id === $currentTab}
            class:text-sm={style === "card"}
            class:border={style === "card"}
            class:rounded-t-md={style === "card"}
            class="group inline-flex items-center font-medium text-sm transition-all"
          >
            {#if tab.icon}
              <span
                class:text-primary-500={tab.id === $currentTab}
                class:text-gray-400={tab.id !== $currentTab}
                class:group-hover:text-gray-500={tab.id !== $currentTab}
                class="mr-2"
              >
                <Icon type={tab.icon} size="5" />
              </span>
            {/if}
            <span>{tab.name}</span>
          </a>
        {/each}
      </nav>
    </div>
  </div>
</div>

{#if style === "card"}
  <div class="bg-white p-4 border shadow rounded-md rounded-tl-none">
    {#if $currentTab !== undefined}
      <slot />
    {:else}
      <div class="hidden">
        <slot />
      </div>
      <slot name="none" />
    {/if}
  </div>
{:else if $currentTab !== undefined}
  <slot />
{:else}
  <div class="hidden">
    <slot />
  </div>
  <slot name="none" />
{/if}
