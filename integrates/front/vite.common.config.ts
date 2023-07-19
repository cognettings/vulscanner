import path from "path";

import react from "@vitejs/plugin-react-swc";
import type { OnResolveResult, Plugin } from "esbuild";
import type { UserConfigExport } from "vite";
import { splitVendorChunkPlugin } from "vite";

const esmPatches: Plugin = {
  name: "esmPatches",
  setup: (build): void => {
    const patches = [
      // https://github.com/bvaughn/react-virtualized/issues/1212
      {
        filter: /react-virtualized/u,
        patch: path.resolve(
          "./node_modules/react-virtualized/dist/umd/react-virtualized.js"
        ),
      },
    ];

    patches.forEach(({ filter, patch }): void => {
      build.onResolve({ filter }, (): OnResolveResult => ({ path: patch }));
    });
  },
};

export const commonConfig: UserConfigExport = {
  build: {
    assetsDir: ".",
    emptyOutDir: true,
    manifest: true,
    outDir: path.resolve(__dirname, "../app/static/dashboard/"),
    rollupOptions: {
      input: {
        app: "./src/app.tsx",
        graphicsForGroup: "./src/graphics/views/group.tsx",
        graphicsForOrganization: "./src/graphics/views/organization.tsx",
        graphicsForPortfolio: "./src/graphics/views/portfolio.tsx",
      },
      output: {
        assetFileNames: (chunkInfo): string => {
          if (chunkInfo.name?.match(/\.(?<ext>gif|jpg|png|svg)$/u)) {
            return "img/[hash][extname]";
          }

          if (chunkInfo.name?.endsWith(".css") === true) {
            return "[name]-vite-style.min.css";
          }

          return "[hash][extname]";
        },
        chunkFileNames: "[name]-vite-bundle.min.js",
        entryFileNames: "[name]-vite-bundle.min.js",
        manualChunks: (id): string | undefined => {
          if (id.includes("node_modules")) {
            return "vendors";
          }

          return undefined;
        },
      },
    },
    sourcemap: true,
    target: "es2019",
  },
  optimizeDeps: {
    esbuildOptions: {
      plugins: [esmPatches],
    },
  },
  plugins: [react(), splitVendorChunkPlugin()],
  resolve: {
    alias: {
      components: path.join(__dirname, "src", "components"),
      context: path.join(__dirname, "src", "context"),
      features: path.join(__dirname, "src", "features"),
      graphics: path.join(__dirname, "src", "graphics"),
      hooks: path.join(__dirname, "src", "hooks"),
      pages: path.join(__dirname, "src", "pages"),
      resources: path.join(__dirname, "src", "resources"),
      scenes: path.join(__dirname, "src", "scenes"),
      store: path.join(__dirname, "src", "store"),
      styles: path.join(__dirname, "src", "styles"),
      typings: path.join(__dirname, "src", "typings"),
      utils: path.join(__dirname, "src", "utils"),
    },
  },
};
