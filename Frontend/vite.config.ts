import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import checker from "vite-plugin-checker";
import tailwindcss from "@tailwindcss/vite";
import path from "path";
import Critters from "critters";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default defineConfig({
  build: {
    cssCodeSplit: false,
  },
  plugins: [
    react(),
    tailwindcss(),
    checker({
      overlay: false,
      eslint: {
        lintCommand: 'eslint "./src/**/*.{ts,tsx}"',
      },
    }),
     {
      name: "vite:critters",
      apply: "build",
      enforce: "post",
      generateBundle: async (_, bundle) => {
        const critters = new (Critters as any)({
          preload: "swap",
          compress: true,
          pruneSource: true,
        });
        for (const file of Object.values(bundle)) {
          if (file.type === "asset" && file.fileName.endsWith(".html")) {
            file.source = await critters.process(file.source as string);
          }
        }
      },
    },
  ],
  server: {
    hmr: { overlay: true },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@shared": path.resolve(__dirname, "./src/shared/"),
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
