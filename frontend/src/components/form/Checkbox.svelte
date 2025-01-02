<script lang="ts">
  export let checked: boolean = null;
  export const id = Math.random().toString(36).slice(2);
</script>

<form>
  <div
    class="flex items-center justify-center"
    on:click={() => (checked = !checked)}
    on:keydown
    role="checkbox"
    aria-checked={checked}
    tabindex="0"
    {id}
  >
    <button
      class="flex size-7 appearance-none items-center justify-center
            rounded-lg bg-white text-primary-600 shadow hover:opacity-75"
      id="checkbox"
    >
      {#if checked === undefined}
        -
      {:else if checked}
        ✓
      {/if}
    </button>
    <label class="pl-4 font-medium text-primary-900" for={id}>
      <slot />
    </label>
  </div>
</form>
