<script lang="ts">
  import { createEventDispatcher, getContext } from "svelte";
  import { fade } from "svelte/transition";
  import { clickOutside } from "../../shared/dom";
  import { shrink, shrinkY } from "../../shared/transitions";
  import Icon from "../Icon.svelte";

  export let options: any[][];
  export let selected: any;
  export let fill = false;
  export let id = "";
  export let disabled = false;
  export let up = false;
  export let wide = false;

  export let autoOpen = false;
  let opened = autoOpen;
  const dispatch = createEventDispatcher();

  let selectedName: any;
  let selectedIndex: any;
  let hoverSelected: any = undefined;
  $: shownSelected = hoverSelected !== undefined ? hoverSelected : selected;
  $: {
    selectedName = "";
    selectedIndex = -1;
    if (options) {
      for (const option of options) {
        const [value, name] = option;
        if (value === shownSelected) {
          selectedName = name;
          selectedIndex = options.indexOf(option);
          break;
        }
      }
    }
  }

  let typedChars = "";
  let typingTimeout: any = null;
  let hasKeyChange = false;
  function onKeyDown(e: any) {
    // Arrow Keys
    if (e.key === "ArrowDown") {
      if (selectedIndex < options.length - 1) {
        hoverSelected = options[selectedIndex + 1][0];
      }
    } else if (e.key === "ArrowUp") {
      if (selectedIndex > 0) {
        hoverSelected = options[selectedIndex - 1][0];
      }
    } else if (e.key === "Enter") {
      opened = false;
      onLoseFocus();
    }
    // Typing name?
    else if (e.key.length === 1) {
      typedChars += e.key.toLowerCase();

      // Select first match
      for (const option of options) {
        const [value, name] = option;
        if (name.toLowerCase().startsWith(typedChars)) {
          hoverSelected = value;
          break;
        }
      }

      // Reset after a small amount of time
      clearTimeout(typingTimeout);
      typingTimeout = setTimeout(() => (typedChars = ""), 1500);
    } else {
      return;
    }

    // Capture key press
    e.preventDefault();
  }

  // Trigger change after key move
  function onLoseFocus() {
    if (hoverSelected !== undefined && hoverSelected !== selected) {
      selected = hoverSelected;
      dispatch("change", selected);
    }
    hoverSelected = undefined;
  }

  export function open() {
    opened = true;
  }
</script>

<div
  class="relative"
  class:w-full={fill}
  class:w-48={wide}
  use:clickOutside={() => {
    opened = false;
  }}
>
  <button
    {id}
    type="button"
    class="relative w-full cursor-default rounded-md border border-gray-300 bg-white py-2 pl-3 pr-10 text-left shadow-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 sm:text-sm"
    aria-haspopup="listbox"
    aria-expanded="true"
    aria-labelledby="listbox-label"
    on:click|preventDefault={() => (opened = !opened)}
    on:keydown={onKeyDown}
    on:blur={onLoseFocus}
    {disabled}
  >
    <span class="block truncate">{selectedName}&nbsp;</span>
    {#if !disabled}
      <span
        class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2"
      >
        <Icon type="ChevronDown" size="5" />
      </span>
    {/if}
  </button>

  {#if opened}
    <div class="overflow-hidden">
      <ul
        class="absolute z-10 mt-1 max-h-60 overflow-y-scroll rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
        class:bottom-10={up}
        tabindex="-1"
        role="listbox"
        aria-labelledby="listbox-label"
        aria-activedescendant="listbox-option-3"
        transition:shrinkY|local
      >
        {#each options as [value, name]}
          <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
          <li
            class="text-gray-900 relative cursor-default select-none py-2 pl-3 pr-9 hover:text-white hover:bg-primary-600"
            on:click={() => {
              selected = value;
              opened = false;
              dispatch("change", value);
            }}
            on:keypress
          >
            <span
              class:font-semibold={value === shownSelected}
              class:font-normal={value !== shownSelected}
              class="block truncate">{name}</span
            >

            {#if value === shownSelected}
              <span
                class="text-primary-600 absolute inset-y-0 right-0 flex items-center pr-4"
              >
                <Icon type="Check" size="5" />
              </span>
            {/if}
          </li>
        {/each}
      </ul>
    </div>
  {/if}
</div>
