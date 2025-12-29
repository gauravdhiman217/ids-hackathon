import type { APIConfig } from "../types";
/**
 * Utility to strongly type and define grouped API endpoints.
 *
 * Usage:
 * const CATEGORY = defineAPIConfig({ ... });
 */
export const defineAPIConfig = <T extends APIConfig>(config: T): T => config;
