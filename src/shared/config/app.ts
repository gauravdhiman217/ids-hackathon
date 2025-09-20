/**
 * Note:
 * - All values are injected at build time via Vite's environment mode.
 * - Ensure that corresponding key-value pairs are defined in the relevant `.env` file
 *   (e.g., .env, .env.production, .env.staging, etc.) depending on your mode.
 *
 * Example:
 *   VITE_API_BASE_URL=https://api.example.com
 *   VITE_APP_NAME=exampleapp
 */

export const appConfig = {
  NODE_ENV: import.meta.env.MODE,
  API_BASE_URL: import.meta.env.VITE_API_BASE_URL,
  APP_NAME: import.meta.env.VITE_APP_NAME,
};
