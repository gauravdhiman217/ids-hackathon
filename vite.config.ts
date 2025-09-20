import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import checker from 'vite-plugin-checker';
import tailwindcss from "@tailwindcss/vite";
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
   checker({
      eslint: {
        lintCommand: 'eslint "./src/**/*.{ts,tsx}"',
      },
    }),
  ],
  server: {
    hmr: { overlay: true },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@shared': path.resolve(__dirname, './src/shared/'),
       /*
        => You can define additional aliases here to mirror what's defined in tsconfig.json

        Examples:
        '@features': path.resolve(__dirname, './src/features/'),
        '@config': path.resolve(__dirname, './src/shared/config/'),
        '@hooks': path.resolve(__dirname, './src/shared/hooks/')
      */
    },
  },
});
