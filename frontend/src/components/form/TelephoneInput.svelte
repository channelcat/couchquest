<script lang="ts">
  import { onMount } from "svelte";
  import Input from "./Input.svelte";

  export let value = "";
  export let isValidNumber = true;
  export let maxlength: number | null = null;

  const intlTelInput = (window as any).intlTelInput;
  const intlTelInputUtils = (window as any).intlTelInputUtils;

  let telephoneInputElement: Element;
  let telephoneInput: any;
  onMount(() => {
    telephoneInput = intlTelInput(telephoneInputElement, {
      allowDropdown: false,
      preferredCountries: ["us"],
    });
  });

  function onChangePhoneNumber() {
    isValidNumber = intlTelInputUtils.isValidNumber(
      telephoneInput.getNumber(),
      "us", // telephoneInput.getSelectedCountryData().iso2
    );
    const formattedNumber = intlTelInputUtils.formatNumber(
      telephoneInput.getNumber(),
      "us", // telephoneInput.getSelectedCountryData().iso2
    );

    telephoneInput.setNumber(formattedNumber);
  }
</script>

{#if value && !isValidNumber}
  <div class="text-sm text-red-500 mb-2">
    Warning, not a valid phone number!
  </div>
{/if}

<Input
  bind:element={telephoneInputElement}
  type="tel"
  {maxlength}
  bind:value
  on:change={onChangePhoneNumber}
/>
