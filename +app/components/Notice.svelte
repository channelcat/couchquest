<script lang="ts">
  import Icon, { type IconType } from "./Icon.svelte";

  export let style: "success" | "info" | "note" | "warning" | "error";
  export let icon: IconType =
    style === "note"
      ? "PencilSquare"
      : style === "error"
        ? "ExclamationCircle"
        : style === "warning"
          ? "ExclamationTriangle"
          : style === "info"
            ? "QuestionMarkCircle"
            : style === "success"
              ? "CheckCircle"
              : "XCircle";
  export let pre = true;
</script>

<div
  class:shadow-green-200={style === "success"}
  class:bg-green-100={style === "success"}
  class:shadow-blue-200={style === "info"}
  class:bg-blue-100={style === "info"}
  class:shadow-yellow-200={style === "note"}
  class:bg-yellow-100={style === "note"}
  class:shadow-orange-200={style === "warning"}
  class:bg-orange-100={style === "warning"}
  class:shadow-red-200={style === "error"}
  class:bg-red-100={style === "error"}
  class="mb-4 shadow p-3 sm:rounded-lg"
>
  <div
    class:text-green-600={style === "success"}
    class:text-blue-600={style === "info"}
    class:text-yellow-600={style === "note"}
    class:text-orange-600={style === "warning"}
    class:text-red-600={style === "error"}
    class="flex items-start"
  >
    <div
      class:bg-green-200={style === "success"}
      class:bg-blue-200={style === "info"}
      class:bg-yellow-200={style === "note"}
      class:bg-orange-200={style === "warning"}
      class:bg-red-200={style === "error"}
      class="flex flex-shrink-0 items-center justify-center rounded-full h-10 w-10"
    >
      <Icon size="6" type={icon} />
    </div>
    <div class="mt-3 mt-0 ml-4 text-left flex self-center">
      <p class="text-sm" class:whitespace-pre-wrap={pre}>
        <slot />
      </p>
    </div>
  </div>
</div>
