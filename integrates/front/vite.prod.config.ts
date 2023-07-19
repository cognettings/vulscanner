import type { UserConfigExport } from "vite";

import { CI_COMMIT_REF_NAME, INTEGRATES_BUCKET_NAME } from "./src/utils/ctx";
import { commonConfig } from "./vite.common.config";

const prodConfig: UserConfigExport = {
  ...commonConfig,
  base: `https://${INTEGRATES_BUCKET_NAME}/${CI_COMMIT_REF_NAME}/static/dashboard/`,
  mode: "production",
};

// eslint-disable-next-line import/no-default-export
export default prodConfig;
