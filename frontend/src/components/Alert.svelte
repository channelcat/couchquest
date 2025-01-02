<script lang="ts" context="module">
  import { writable } from "svelte/store";

  export let alert = writable(null);

  type Options = {
    title?: string;
    html?: boolean;
    wide?: boolean;
    image?: string;
    destructive?: boolean;
    confirmText?: string;
  };

  export function showError(
    description: string,
    {
      title = "Error",
      html = false,
      wide = false,
      destructive = true,
      confirmText = "OK",
      image = null,
    }: Options = {},
  ) {
    alert.set({
      type: "error",
      title,
      description,
      html,
      wide,
      destructive,
      confirmText,
      image,
    });
  }
  export function showNotice(
    description: string,
    {
      title = "",
      html = false,
      wide = false,
      destructive = false,
      confirmText = "OK",
      image = null,
    }: Options = {},
  ) {
    alert.set({
      type: "notice",
      title,
      description,
      html,
      wide,
      destructive,
      confirmText,
      image,
    });
  }
  export function showConfirm(
    description: string,
    onConfirm: () => void,
    {
      title = "",
      html = false,
      wide = false,
      destructive = false,
      confirmText = "Continue",
      image = null,
    }: Options = {},
  ) {
    alert.set({
      type: "confirm",
      title,
      description,
      html,
      wide,
      destructive,
      onConfirm,
      confirmText,
      image,
    });
  }
</script>

<script lang="ts">
  import { fade, scale } from "svelte/transition";
  import Icon from "./Icon.svelte";

  function close() {
    $alert = null;
  }
  function confirm() {
    const onConfirm = $alert?.onConfirm;
    close();
    if (onConfirm) {
      onConfirm();
    }
  }
  function handleKeydown(e: KeyboardEvent) {
    if ($alert) {
      if (e.key == "Enter" || e.key == "Escape") {
        e.stopPropagation();
        e.preventDefault();
        $alert = null;
      }
    }
  }
</script>

<svelte:window on:keydown={handleKeydown} />
{#if $alert}
  <div
    class="relative z-30"
    aria-labelledby="modal-title"
    role="dialog"
    aria-modal="true"
    in:fade={{ duration: 300 }}
    out:fade={{ duration: 200 }}
  >
    <div class="fixed inset-0 bg-white bg-opacity-75 transition-opacity" />

    <div class="fixed inset-0 z-20 overflow-y-auto">
      <div
        class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0"
      >
        <div
          in:scale={{ duration: 300 }}
          out:scale={{ duration: 200 }}
          class:sm:max-w-lg={!$alert.wide}
          class:sm:max-w-6xl={$alert.wide}
          class="relative transform overflow-hidden rounded-lg bg-white px-4 pt-5 pb-4 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:p-6"
        >
          <div class="absolute top-0 right-0 hidden pt-4 pr-4 sm:block">
            <button
              on:click={close}
              type="button"
              class="rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
            >
              <span class="sr-only">Close</span>
              <Icon size="6" type="XMark" />
            </button>
          </div>
          <div class="sm:flex sm:items-start">
            {#if $alert.type === "error"}
              <div
                class="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10"
              >
                <Icon
                  class="text-red-600"
                  size="6"
                  type="ExclamationTriangle"
                />
              </div>
            {/if}
            <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
              <h3
                class="text-lg font-medium leading-6 text-gray-900"
                id="modal-title"
              >
                {$alert.title}
              </h3>
              <div class="mt-2">
                {#if $alert.image}
                  <img
                    src={$alert.image}
                    alt={$alert.title}
                    class="max-w-full max-h-64 mb-4 mx-auto"
                  />
                {/if}
                {#if $alert.description}
                  {#if $alert.html}
                    <span class="text-sm text-gray-500">
                      {@html $alert.description}
                    </span>
                  {:else}
                    <p class="text-sm text-gray-500 whitespace-pre-wrap">
                      {$alert.description}
                    </p>
                  {/if}
                {/if}
              </div>
            </div>
          </div>
          <div class="mt-5 sm:mt-4 sm:flex sm:flex-row-reverse">
            <button
              on:click={confirm}
              type="button"
              class:bg-primary-600={!$alert.destructive}
              class:hover:bg-primary-700={!$alert.destructive}
              class:focus:ring-primary-500={!$alert.destructive}
              class:bg-red-600={$alert.destructive}
              class:hover:bg-red-700={$alert.destructive}
              class:focus:ring-red-500={$alert.destructive}
              class="inline-flex w-full justify-center rounded-md border px-4 py-2 text-base font-medium text-white shadow-sm border-transparent focus:outline-none focus:ring-2 focus:ring-offset-2 sm:ml-3 sm:w-auto sm:text-sm"
            >
              {$alert.confirmText}
            </button>
            {#if $alert.type === "confirm"}
              <button
                on:click={close}
                type="button"
                class="inline-flex w-full justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-base font-medium text-gray-700 shadow-sm hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 mt-3 sm:mt-0 sm:w-auto sm:text-sm"
              >
                Cancel
              </button>
            {/if}
          </div>
        </div>
      </div>
    </div>
  </div>
{/if}
