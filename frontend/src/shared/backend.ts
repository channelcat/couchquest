// TODO: custom adapter

import { showError, showNotice } from "../components/Alert.svelte";

export async function apiCall<A, R>(
  call: (data: A) => Promise<R>,
  data: A = undefined,
  options: { handleError?: boolean } = { handleError: true },
): Promise<[R | null, string | null]> {
  let result = null;
  let error = null;
  try {
    result = await call(data);
  } catch (e: any) {
    error = e?.body?.error?.message || `Unknown error: ${e}`;
    if (options.handleError) {
      if (e?.body?.error?.code === "fulfilled") {
        showNotice(error);
      } else {
        showNotice(error, { destructive: true });
      }
    }
  }
  return [result, error];
}