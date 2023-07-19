import type {
  ColumnDef,
  ColumnFiltersState,
  VisibilityState,
} from "@tanstack/react-table";
import type { Dispatch, SetStateAction } from "react";

import type {
  IHistoricTreatment,
  IVulnerabilityCriteriaData,
  IVulnerabilityCriteriaRequirement,
} from "scenes/Dashboard/containers/Finding-Content/DescriptionView/types";
import type { IFinding } from "scenes/Dashboard/containers/Group-Content/GroupVulnerabilitiesView/types";
import type { IOrganizationGroups } from "scenes/Dashboard/types";

enum vulnerabilityStates {
  REJECTED = "REJECTED",
  SAFE = "SAFE",
  SUBMITTED = "SUBMITTED",
  VULNERABLE = "VULNERABLE",
}

type vulnerabilityStatesStrings = keyof typeof vulnerabilityStates;

interface IFormatVulns {
  requirementsData?: Record<string, IVulnerabilityCriteriaRequirement>;
  vulnerabilities: IVulnRowAttr[];
  vulnsData?: Record<string, IVulnerabilityCriteriaData>;
}
interface IFormatVulnsTreatment {
  organizationsGroups?: IOrganizationGroups[];
  vulnerabilities: IVulnRowAttr[];
}

interface IGetVulnById {
  vulnerabilities: IVulnRowAttr[];
  vulnerabilityId: string;
}

interface IVulnerabilityAdvisories {
  cve: string[];
  package: string;
  vulnerableVersion: string;
}

interface IVulnRowAttr {
  advisories: IVulnerabilityAdvisories | null;
  acceptance?: "" | "APPROVED" | "REJECTED";
  externalBugTrackingSystem: string | null;
  findingId: string;
  groupName: string;
  hacker?: string;
  organizationName: string | undefined;
  historicTreatment: IHistoricTreatment[];
  id: string;
  lastStateDate: string;
  lastTreatmentDate: string;
  lastVerificationDate: string | null;
  remediated: boolean;
  reportDate: string | null;
  rootNickname: string | null;
  severity: string | null;
  severityTemporalScore: number;
  source: string;
  sourceType?: string;
  specific: string;
  state: vulnerabilityStatesStrings;
  stream: string | null;
  tag: string;
  technique: string;
  treatmentDate: string;
  treatmentAcceptanceDate: string | null;
  treatmentAcceptanceStatus: string | null;
  treatmentAssigned: string | null;
  treatmentJustification: string | null;
  treatmentStatus: string;
  treatmentUser: string | null;
  assigned: string;
  verification: string | null;
  vulnerabilityType: string;
  where: string;
  zeroRisk: string | null;
  finding?: IFinding;
  requirements?: string[];
}

interface IUploadVulnerabilitiesResultAttr {
  uploadFile: {
    success: boolean;
    message?: string;
  };
}

interface IDownloadVulnerabilitiesResultAttr {
  downloadVulnerabilityFile: {
    success: boolean;
    url: string;
  };
}

interface IVulnDataTypeAttr {
  externalBugTrackingSystem: string | null;
  findingId: string;
  groupName: string;
  historicTreatment: IHistoricTreatment[];
  id: string;
  severity: string | null;
  source: string;
  specific: string;
  state: vulnerabilityStatesStrings;
  tag: string;
  assigned: string;
  where: string;
}

interface IVulnComponentProps {
  clearFiltersButton?: () => void;
  changePermissions?: (groupName: string) => void;
  columnFilterSetter?: Dispatch<SetStateAction<ColumnFiltersState>>;
  columnFilterState?: ColumnFiltersState;
  columnToggle?: boolean;
  columnDefaultVisibility?: VisibilityState;
  columns: ColumnDef<IVulnRowAttr>[];
  csvColumns?: string[];
  csvHeaders?: Record<string, string>;
  enableColumnFilters?: boolean;
  exportCsv?: boolean;
  extraButtons?: JSX.Element;
  filters?: JSX.Element;
  findingState?: "SAFE" | "VULNERABLE";
  id: string;
  isClosing?: boolean;
  isFindingReleased?: boolean;
  isEditing: boolean;
  isRequestingReattack: boolean;
  isResubmitting?: boolean;
  isVerifyingRequest: boolean;
  isUpdatingSeverity?: boolean;
  refetchData: () => void;
  hasNextPage?: boolean;
  size?: number;
  nonValidOnReattackVulnerabilities?: IVulnRowAttr[];
  vulnerabilities: IVulnRowAttr[];
  onNextPage?: () => Promise<void>;
  onSearch?: (search: string) => void;
  onVulnSelect?: (
    vulnerabilities: IVulnRowAttr[],
    clearSelected: () => void
  ) => void;
  vulnData?: Record<string, IVulnerabilityCriteriaData>;
  requirementData?: Record<string, IVulnerabilityCriteriaRequirement>;
}

interface IUpdateVulnerabilityForm {
  acceptanceDate?: string;
  externalBugTrackingSystem: string | null;
  justification?: string;
  severity: string | null;
  source?: string;
  tag?: string;
  treatment: string;
  assigned?: string;
}

interface IVulnerabilityModalValues
  extends Array<
    | IUpdateVulnerabilityForm
    | React.Dispatch<React.SetStateAction<IUpdateVulnerabilityForm>>
  > {
  0: IUpdateVulnerabilityForm;
  1: React.Dispatch<React.SetStateAction<IUpdateVulnerabilityForm>>;
}

export type {
  IFormatVulns,
  IFormatVulnsTreatment,
  IGetVulnById,
  IVulnRowAttr,
  IUploadVulnerabilitiesResultAttr,
  IDownloadVulnerabilitiesResultAttr,
  IVulnerabilityModalValues,
  IUpdateVulnerabilityForm,
  IVulnDataTypeAttr,
  IVulnComponentProps,
  vulnerabilityStatesStrings,
};

export { vulnerabilityStates };
