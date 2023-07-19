import type {
  IVulnerabilityCriteriaData,
  IVulnerabilityCriteriaRequirement,
} from "scenes/Dashboard/containers/Finding-Content/DescriptionView/types";

interface IReqFormat {
  findingTitle: string | undefined;
  vulnsData?: Record<string, IVulnerabilityCriteriaData>;
  requirementsData?: Record<string, IVulnerabilityCriteriaRequirement>;
}

interface IReqFormatProps {
  reqsList: string[] | undefined;
}

export type { IReqFormat, IReqFormatProps };
