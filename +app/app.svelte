<script lang="ts">
  import { setupClient } from "@coloco/api-client-svelte";
  import { route, Router, getRoutes } from "./router";

  import Index from "./index.svelte";
  import NotFound from "./404.svelte";
  import Example from "../example/index.svelte";
  setupClient({
    baseUrl: "http://localhost:5172",
  });
  const routes = getRoutes({
    index: Index,
    notFound: NotFound,
  });
  console.log(routes);
</script>

<main>
  Main Page

  <br /><br />

  <a use:route href="/">Home</a><br />
  <a use:route href="/example">Example</a><br />
  <a use:route href="/missing">Missing</a>

  <br /><br />

  <Router basePath="/" {routes} />
</main>
