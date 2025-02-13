<script lang="ts">
  import { onMount } from "svelte";
  import { waitFor } from "../../shared/utils";
  import { apiCall } from "../../shared/backend";
  import { googleOauthCallback } from "../../backend";

  export let clientId: string;

  async function googleLogin(token: string) {
    const [response, error] = await apiCall(googleOauthCallback, {
      requestBody: { token },
    });
    if (error) {
      console.error(error);
    }
    console.log(response);
  }

  async function onGoogleSignin(result: any) {
    loggingIn = true;
    console.log("onGoogleSignin", result);
    await googleLogin(result.credential);
  }

  let googleButton: HTMLDivElement;
  let loggingIn = false;
  onMount(async () => {
    const googleAccounts = await waitFor(() => window.google?.accounts?.id);
    // Docs: https://developers.google.com/identity/gsi/web/reference/js-reference
    googleAccounts.initialize({
      client_id: clientId,
      callback: onGoogleSignin,
    });
    googleAccounts.renderButton(googleButton, { type: "standard" });
  });
</script>

<svelte:head>
  <script src="https://accounts.google.com/gsi/client" async></script>
</svelte:head>

<div bind:this={googleButton}>
  <!-- Google Login Button -->
</div>
