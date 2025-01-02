<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import Icon, { type IconType } from "../Icon.svelte";

  const dispatch = createEventDispatcher();

  export let preventDefault = false;
  export let stopPropagation = false;
  export let disabled = null;
  export let center = false;
  export let right = false;
  export let fill = false;
  export let icon: IconType = null;
  export let iconComponent: any = null;
  export let iconLight = false;
  export let inline = true;
  export let loading = false;
  export let animateIcon: false | "spin" | "ping" | "pulse" | "bounce" = false;
  export let size: "sm" | "md" | "lg" | "xl" = "md";
  export let style: "primary" | "secondary" | "form" | "warning" | "danger" =
    "primary";

  const iconSizes = {
    sm: "4",
    md: "5",
    lg: "6",
    xl: "7",
  };
  $: iconSize = iconSizes[size];
  $: isDisabled = disabled || loading;
  $: useIconType = icon || (loading ? "ArrowPath" : null);

  // Force icon color update for svg
  // TODO: find a better way to color svg
  let textColor: string = null;
  let buttonElement: HTMLElement = null;
  function setTextColor(buttonElement: HTMLElement) {
    if (buttonElement) {
      textColor = getComputedStyle(buttonElement).color;
    }
  }
  function updateColor(disabled: boolean, loading: boolean) {
    if (buttonElement) {
      const interval = setInterval(() => setTextColor(buttonElement), 30);
      setTimeout(() => clearInterval(interval), 200);
    }
  }
  $: setTextColor(buttonElement);
  $: updateColor(isDisabled, loading);
</script>

<button
  {...$$props}
  on:click={(e) => {
    if (preventDefault) {
      e.preventDefault();
    }
    if (stopPropagation) {
      e.stopPropagation();
    }
    dispatch("click");
  }}
  bind:this={buttonElement}
  type="submit"
  disabled={isDisabled}
  class:justify-center={center}
  class:rounded-r-md={right}
  class:rounded-md={!right}
  class:w-full={fill}
  class:flex={!inline}
  class:inline-flex={inline}
  class:hover:bg-primary-500={!isDisabled && style === "primary"}
  class:bg-primary-400={!isDisabled && style === "primary"}
  class:text-primary-50={!isDisabled && style === "primary"}
  class:hover:bg-gray-500={!isDisabled && style === "secondary"}
  class:bg-gray-400={!isDisabled && style === "secondary"}
  class:text-gray-800={!isDisabled && style === "secondary"}
  class:hover:bg-red-700={!isDisabled && style === "danger"}
  class:bg-red-600={!isDisabled && style === "danger"}
  class:text-white={!isDisabled && style === "danger"}
  class:focus:ring-red-500={!isDisabled && style === "danger"}
  class:hover:bg-yellow-400={!isDisabled && style === "warning"}
  class:bg-yellow-300={!isDisabled && style === "warning"}
  class:text-yellow-700={!isDisabled && style === "warning"}
  class:focus:ring-yellow-500={!isDisabled && style === "warning"}
  class:hover:bg-gray-50={!isDisabled && style === "form"}
  class:border-gray-300={!isDisabled && style === "form"}
  class:bg-white={!isDisabled && style === "form"}
  class:text-gray-700={!isDisabled && style === "form"}
  class:shadow-sm={!isDisabled && style === "form"}
  class:leading-4={!isDisabled && style === "form"}
  class:bg-gray-300={isDisabled}
  class:text-gray-500={isDisabled}
  class:px-3={(!isDisabled && style === "form") ||
    (size === "sm" && $$slots.default)}
  class:px-1={size === "sm" && !$$slots.default}
  class:py-1={size === "sm"}
  class:text-xs={size === "sm"}
  class:px-4={size === "md" && $$slots.default}
  class:px-2={size === "md" && !$$slots.default}
  class:py-2={size === "md"}
  class:text-sm={size === "md"}
  class:px-6={size === "xl"}
  class:py-3={size === "xl"}
  class:text-xl={size === "xl"}
  class="group whitespace-nowrap relative border border-transparent py-2 px-4 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 items-center transition-all"
>
  {#if useIconType || iconComponent}
    <span
      class:text-primary-300={!isDisabled && iconLight && style === "primary"}
      class:text-primary-600={!isDisabled && !iconLight && style === "primary"}
      class:group-hover:text-primary-400={!isDisabled &&
        iconLight &&
        style === "primary"}
      class:group-hover:text-primary-700={!isDisabled &&
        !iconLight &&
        style === "primary"}
      class:text-gray-300={!isDisabled && iconLight && style === "form"}
      class:text-gray-500={!isDisabled && !iconLight && style === "form"}
      class:group-hover:text-gray-400={!isDisabled &&
        iconLight &&
        style === "form"}
      class:group-hover:text-gray-600={!isDisabled &&
        !iconLight &&
        style === "form"}
      class:text-gray-400={isDisabled}
      class:animate-spin={animateIcon === "spin" || loading}
      class:animate-ping={animateIcon === "ping"}
      class:animate-pulse={animateIcon === "pulse"}
      class:animate-bounce={animateIcon === "bounce"}
    >
      {#if iconComponent}
        <svelte:component this={iconComponent} color={textColor} />
      {:else}
        <Icon type={useIconType} theme="solid" size={parseInt(iconSize)} />
      {/if}
    </span>
    <span>&nbsp;<slot /></span>
  {:else}
    <slot />
  {/if}
</button>
