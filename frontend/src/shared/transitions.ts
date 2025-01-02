
import { cubicOut } from 'svelte/easing';

// Transitions
export function shrink(node: Element, { delay = 0, duration = 200, useMax = true, x = true, y = true, autoOverflow = true } = {}) {
  const matchWidth = getComputedStyle(node).width.match(/^(\d+)(.+?)$/);
  const matchHeight = getComputedStyle(node).height.match(/^(\d+)(.+?)$/);
  const width = matchWidth ? +matchWidth[1] : 0;
  const widthUnits = matchWidth ? matchWidth[2] : "px";
  const height = matchHeight ? +matchHeight[1] : 0;
  const heightUnits = matchHeight ? matchHeight[2] : "px";
  const max = useMax ? 'max-' : '';
  const overflow = autoOverflow ? "overflow:hidden;" : "";

  const getX = (t: number) => `${max}width: ${Math.trunc(t * width)}${widthUnits};`
  const getY = (t: number) => `${max}height: ${Math.trunc(t * height)}${heightUnits};`

  return {
    delay,
    duration,
    css: (t: number) => {
      const eased = cubicOut(t);
      return `${x ? getX(eased) : ""}${y ? getY(eased) : ""}${overflow}`
    },
  };
}

export function shrinkY(node: Element, options = {}) {
  return shrink(node, { ...options, x: false, y: true });
}

export function shrinkX(node: Element, options = {}) {
  return shrink(node, { ...options, x: true, y: false });
}

export function css(node: Element, { duration, direction, ...props }: { duration?: number, direction?: "in" | "out", [x: string]: any; }) {
  const cssProps: any = [];
  duration = duration ?? 0;
  for (const [key, value] of Object.entries(props)) {
    if (typeof value === "number") {
      cssProps.push([key, value, ""]);
    } else {
      const match = value.match(/^([0-9\.\-]+)(.+?)$/);
      if (match) {
        cssProps.push([key, match[1], match[2]]);
      } else {
        console.error("Unknown css value" + value);
      }
    }
  }
  return {
    duration,
    css: (t: number) => {
      const eased = direction === "out" ? 1 - cubicOut(t) : cubicOut(t);
      return cssProps
        .map(([key, value, unit]: any) => `${key}: ${value * eased}${unit}`)
        .join("\n");
    },
  };
}

export function hide(node: Element) {
  return {
    duration: 0,
    css: (t: number) => {
      // display doesn't work, so throw everything else at it
      return "overflow:hidden; width:0; height:0; margin:0; padding:0; position:absolute; opacity: 0;"
    },
  };
}