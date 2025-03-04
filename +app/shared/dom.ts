// Generates a guaranteed unique ID
export function getUniqueElementId(prefix: string) {
  let id;
  while (!id || document.getElementById(id)) {
    id = prefix + "-" + Math.floor(Math.random() * 1000000000);
  }
  return id;
}

// Svelte event
export function clickOutside(element: HTMLElement, callbackFunction: () => void) {
  function onClick(event: any) {
    if (!element.contains(event.target)) {
      callbackFunction();
    }
  }

  document.body.addEventListener('click', onClick);

  return {
    update(newCallbackFunction: () => void) {
      callbackFunction = newCallbackFunction;
    },
    destroy() {
      document.body.removeEventListener('click', onClick);
    }
  }
}

export function downloadURL(url: string, filename: string = null) {
  const anchor = document.createElement("a");
  anchor.href = url;
  if (filename)
    anchor.setAttribute("download", filename);
  anchor.click();
}

export function download(blob: Blob | MediaSource, filename: string) {
  const anchor = document.createElement("a");
  anchor.href = URL.createObjectURL(blob);
  anchor.setAttribute("download", filename);
  anchor.click();
}