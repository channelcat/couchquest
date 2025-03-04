<script lang="ts" context="module">
  import { writable } from "svelte/store";

  type Toast = {
    id: number;
    icon?: IconType;
    message: string;
    description: string;
    timeout?: any;
    type: "notice" | "error" | "success";
  };

  export function showToast(
    message: string,
    {
      description = undefined,
      type = "notice",
      duration = 3000,
      icon = undefined,
    }: {
      description?: string;
      type?: "notice" | "error" | "success";
      duration?: number;
      icon?: IconType;
    } = {},
  ) {
    const toast: Toast = { id: ++lastId, message, description, type, icon };
    if (duration) {
      toast.timeout = setTimeout(() => removeToast(toast), duration);
    }
    toasts.set([..._toasts, toast]);
    return toast;
  }

  export function removeToast(toast: Toast) {
    if (toast.timeout) {
      clearTimeout(toast.timeout);
    }
    _toasts.splice(_toasts.indexOf(toast), 1);
    toasts.set(_toasts);
  }

  let lastId = 0;
  let _toasts: Toast[];
  let toasts = writable<Toast[]>([]);
  toasts.subscribe((t) => (_toasts = t));
</script>

<script lang="ts">
  import { fade, fly } from "svelte/transition";
  import { flip } from "svelte/animate";
  import Icon, { type IconType } from "./Icon.svelte";
</script>

<div
  aria-live="assertive"
  class="pointer-events-none fixed inset-0 flex items-end px-4 py-6 sm:items-start sm:p-6 z-50"
>
  <div class="flex w-full flex-col items-center space-y-4 sm:items-end">
    {#each $toasts as toast (toast.id)}
      <div
        in:fly={{ x: 256, duration: 200 }}
        out:fade={{ duration: 200 }}
        animate:flip={{ duration: 200 }}
        class="pointer-events-auto w-full max-w-sm overflow-hidden rounded-lg bg-white shadow-lg ring-1 ring-black ring-opacity-5"
      >
        <div class="p-4">
          <div class="flex items-start">
            <div
              class:text-green-500={toast.type === "success"}
              class:text-red-500={toast.type === "error"}
              class="flex-shrink-0 text-gray-500 -mt-0.5"
            >
              {#if toast.icon}
                <Icon size="6" type={toast.icon} />
              {:else if toast.type === "success"}
                <Icon size="6" type="CheckCircle" />
              {:else if toast.type === "error"}
                <Icon size="6" type="ExclamationTriangle" />
              {/if}
            </div>
            <div class="ml-3 w-0 flex-1 pt-0.5">
              <p class="text-sm font-medium text-gray-900">
                {toast.message}
              </p>
              {#if toast.description}
                <p class="mt-1 text-sm text-gray-500">
                  {toast.description}
                </p>
              {/if}
            </div>
            <div class="ml-4 flex flex-shrink-0">
              <button
                type="button"
                on:click|preventDefault={() => removeToast(toast)}
                class="inline-flex rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
              >
                <span class="sr-only">Close</span>
                <Icon type="XMark" size="5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    {/each}
  </div>
</div>
