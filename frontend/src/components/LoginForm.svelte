<script lang="ts">
  import { onMount } from "svelte";
  import Loading from "./Loading.svelte";
  import GoogleLogin from "./login/GoogleLogin.svelte";
  import { apiCall } from "../shared/backend";
  import { getProviders, type Providers } from "../backend";

  let loading = false;
  let providers: Providers | null = null;

  onMount(async () => {
    loading = true;
    const [results] = await apiCall(getProviders);
    providers = results;
    loading = false;
  });
</script>

<Loading {loading}>
  <GoogleLogin clientId={providers?.google.client_id} />
</Loading>
