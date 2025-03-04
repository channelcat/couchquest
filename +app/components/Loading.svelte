<script lang="ts">
  import { fade } from "svelte/transition";
  import WavyText from "./WavyText.svelte";
  import Header from "./Header.svelte";

  export let loading = false;
  export let alwaysShowContent = false;
</script>

{#if !loading || alwaysShowContent}
  <slot />
{/if}

{#if loading}
  <div class="fixed inset-0 z-10">
    <div transition:fade={{ duration: 300 }}>
      <div class="bg-white bg-opacity-80 absolute inset-0 z-30"></div>
      <div
        class="absolute inset-0 z-50 flex flex-col items-center justify-center"
      >
        <Header>
          <span style="font-size: min(3vw, 3vh) !important; color: #6994b7;">
            <WavyText>Loading...</WavyText>
          </span>
        </Header>
      </div>
    </div>
  </div>
{/if}
