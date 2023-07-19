import type { UserConfigExport } from "vite";

import { commonConfig } from "./vite.common.config";

const devConfig: UserConfigExport = {
  ...commonConfig,
  mode: "development",
  preview: {
    headers: { "Access-Control-Allow-Origin": "https://localhost:8001" },
    https: {
      cert: process.env.FI_WEBPACK_TLS_CERT,
      key: process.env.FI_WEBPACK_TLS_KEY,
    },
    port: 3000,
    strictPort: true,
  },
  server: {
    headers: { "Access-Control-Allow-Origin": "https://localhost:8001" },
    https: {
      cert: process.env.FI_WEBPACK_TLS_CERT,
      key: process.env.FI_WEBPACK_TLS_KEY,
    },
    origin: "https://localhost:3000",
    port: 3000,
    strictPort: true,
  },
};

// eslint-disable-next-line import/no-default-export
export default devConfig;
