<script lang="ts">
  import { onMount } from "svelte";

  export let duration = 1;

  let textElement: HTMLDivElement;
  let text = "";
  onMount(() => {
    text = textElement.innerText;
  });
</script>

<div class="wavy">
  {#each text as letter, i}
    <span
      style="animation-delay: {(i * duration) /
        text.length}s; animation-duration: {duration}s;">{letter}</span
    >
  {/each}
</div>

<div class="hidden" bind:this={textElement}>
  <slot />
</div>

<style type="text/css">
  .wavy {
    position: relative;
  }

  .wavy span {
    position: relative;
    display: inline-block;
    font-size: 2em;
    text-transform: uppercase;
    animation: animate ease-in-out infinite;
  }

  @keyframes animate {
    0% {
      transform: translateY(0px);
    }

    20% {
      transform: translateY(-20px);
    }

    40%,
    100% {
      transform: translateY(0px);
    }
  }
</style>
