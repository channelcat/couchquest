<script lang="ts">
  import { createEventDispatcher, getContext } from "svelte";
  import Icon, { type IconType } from "../Icon.svelte";

  export let id = getContext<string>("field-id");
  export let full = false;
  export let disabled = false;
  export let type = "text";
  export let tall = false;
  export let step: string = undefined;
  export let both = false;
  export let top = false || both;
  export let bottom = false || both;
  export let left = false;
  export let right = false;
  export let fill = false;
  export let showPercent = false;
  export let min = 0;
  export let max = 2147483647;
  export let icon: IconType = null;
  export let value: string | number = "";

  const dispatch = createEventDispatcher();

  function onChange(e: any) {
    if (type === "number" && typeof value !== "number") {
      if (step && step.indexOf(".") !== -1) {
        const precision = step.split(".")[1].length;
        value = parseFloat(value).toFixed(precision);
      } else {
        value = parseInt(value);
      }
    }
    dispatch("change", value);
  }
</script>

<div class="flex flex-grow" class:space-x-3={type === "range"}>
  {#if type === "range"}
    <output class="block text-center w-100 font-bold text-xl whitespace-nowrap">
      {value || "Use Slider"}{#if showPercent}%{/if}
    </output>
  {/if}
  {#if icon}
    <div class="relative flex flex-grow items-stretch focus-within:z-10">
      <div
        class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3"
      >
        <Icon type={icon} theme="solid" size="5" class="text-gray-400" />
      </div>
    </div>
  {/if}
  {#if full}
    <textarea
      {...{
        ...$$props,
        id,
        disabled,
        icon: null,
        top: null,
        bottom: null,
        left: null,
        right: null,
        fill: null,
      }}
      class:rounded-t-md={top}
      class:rounded-b-md={bottom}
      class:rounded-l-md={left}
      class:rounded-r-md={right}
      class:w-full={fill}
      class:pl-10={icon}
      class:focus:border-primary-500={!disabled}
      class:focus:outline-none={!disabled}
      class:focus:ring-primary-500={!disabled}
      class:text-gray-900={!disabled}
      class:bg-gray-200={disabled}
      class:text-gray-400={disabled}
      class:h-96={tall}
      on:change={onChange}
      on:input
      bind:value
      class="block appearance-none rounded-none border border-gray-300 px-3 py-2 placeholder-gray-500 sm:text-sm"
    />
  {:else}
    <input
      {...{
        ...$$props,
        id,
        disabled,
        icon: null,
        top: null,
        bottom: null,
        left: null,
        right: null,
        fill: null,
      }}
      class:rounded-t-md={top}
      class:rounded-b-md={bottom}
      class:rounded-l-md={left}
      class:rounded-r-md={right}
      class:w-full={fill}
      class:pl-10={icon}
      class:focus:border-primary-500={!disabled}
      class:focus:outline-none={!disabled}
      class:focus:ring-primary-500={!disabled}
      class:text-gray-900={!disabled}
      class:bg-gray-200={disabled}
      class:text-gray-400={disabled}
      bind:value
      on:change={onChange}
      on:input
      {min}
      {max}
      class="block appearance-none rounded-none border border-gray-300 px-3 py-2 placeholder-gray-500 sm:text-sm"
    />
  {/if}
</div>
