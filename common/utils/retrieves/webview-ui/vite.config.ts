import react from "@vitejs/plugin-react";
import path from "path";
import { defineConfig } from "vite";

export default defineConfig({
  build: {
    outDir: `../../dist`,
    target: "es2022",
    rollupOptions: {
      output: {
        assetFileNames: "assets/[name].[ext]",
        chunkFileNames: "assets/[name].js",
        entryFileNames: "webview.js",
      },
      external: ["commonjs vscode", "vscode"],
    },
  },
  resolve: {
    alias: {
      "@retrieves": path.resolve(__dirname, "../src"),
      "@webview": path.resolve(__dirname, "src"),
    }
  },
  root: `${__dirname}/src`,
  plugins: [react()],
  server: {
    headers: {
      "Access-Control-Allow-Origin": "*",
    },
    hmr: {
      host: "localhost",
      protocol: "ws",
    },
    port: 9000,
    strictPort: true,
  },
});
