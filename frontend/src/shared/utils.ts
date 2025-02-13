export function range(num: number) {
  return Array.from(Array(num).keys());
}

export function asyncTimeout(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/* Waits for a function call to return true, then returns the result */
export async function waitFor<T>(callable: () => T, interval = 100, timeout = 30000): Promise<T> {
  let waited = 0;
  let result = callable();
  while (!result) {
    if (waited >= timeout) {
      throw new Error("Timed out waiting for result");
    }
    await asyncTimeout(interval);
    waited += interval;
    result = callable();
  }
  return result;
}