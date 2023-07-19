import type { ArrayHelpers } from "formik";

import type { IIntegrationRepository } from "../../types";

interface IBranchesSectionProps {
  branchesArrayHelpersRef: React.MutableRefObject<ArrayHelpers | null>;
  envsArrayHelpersRef: React.MutableRefObject<ArrayHelpers | null>;
  repositories: Record<string, IIntegrationRepository>;
}

export type { IBranchesSectionProps };
