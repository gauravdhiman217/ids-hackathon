import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Combines class names using clsx and merges Tailwind classes safely.
 * Usage: cn('bg-white', condition && 'text-red-500')
 */

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
