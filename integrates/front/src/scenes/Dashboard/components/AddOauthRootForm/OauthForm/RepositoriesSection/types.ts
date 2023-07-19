import type { ArrayHelpers } from "formik";

import type { IIntegrationRepository } from "../../types";

interface IRepositoriesSectionProps {
  branchesArrayHelpersRef: React.MutableRefObject<ArrayHelpers | null>;
  credentialName: string;
  envsArrayHelpersRef: React.MutableRefObject<ArrayHelpers | null>;
  exclusionsArrayHelpersRef: React.MutableRefObject<ArrayHelpers | null>;
  repositories: Record<string, IIntegrationRepository>;
}

export type { IRepositoriesSectionProps };
