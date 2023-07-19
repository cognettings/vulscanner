import type { ExecutionResult } from "graphql";

import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import type { IFinding } from "scenes/Dashboard/containers/Group-Content/GroupVulnerabilitiesView/types";

interface IVulnDataAttr {
  acceptance: "" | "APPROVED" | "REJECTED";
  finding?: IFinding;
  findingId: string;
  groupName?: string;
  id: string;
  severityTemporalScore: number;
  specific: string;
  where: string;
}

interface IFormValues {
  justification: string;
}

interface IHandleVulnerabilitiesAcceptanceModalProps {
  findingId?: string;
  groupName: string;
  vulns: IVulnRowAttr[];
  handleCloseModal: () => void;
  refetchData: () => void;
}

interface IHandleVulnerabilitiesAcceptanceModalFormProps {
  acceptanceVulnerabilities: IVulnDataAttr[];
  acceptedVulnerabilities: IVulnDataAttr[];
  rejectedVulnerabilities: IVulnDataAttr[];
  hasAcceptedVulns: boolean;
  hasRejectedVulns: boolean;
  handlingAcceptance: boolean;
  confirmingZeroRisk: boolean;
  rejectingZeroRisk: boolean;
  setAcceptanceVulns: React.Dispatch<React.SetStateAction<IVulnDataAttr[]>>;
  treatment: string;
  handleCloseModal: () => void;
  vulns: IVulnRowAttr[];
}

interface IHandleVulnerabilitiesAcceptanceResultAttr {
  handleVulnerabilitiesAcceptance: {
    success: boolean;
  };
}

interface IConfirmVulnerabilitiesResultAttr {
  confirmVulnerabilities: {
    success: boolean;
  };
}

type VulnUpdateResult =
  ExecutionResult<IHandleVulnerabilitiesAcceptanceResultAttr>;

interface IConfirmVulnZeroRiskResultAttr {
  confirmVulnerabilitiesZeroRisk: {
    success: boolean;
  };
}

interface IRejectZeroRiskVulnResultAttr {
  rejectVulnerabilitiesZeroRisk: {
    success: boolean;
  };
}

interface IRejectVulnerabilitiesResultAttr {
  rejectVulnerabilities: {
    success: boolean;
  };
}

interface IAcceptanceVulns extends IVulnDataAttr {
  acceptanceStatus: "APPROVED" | "REJECTED";
}

export type {
  IConfirmVulnerabilitiesResultAttr,
  IConfirmVulnZeroRiskResultAttr,
  IFormValues,
  IHandleVulnerabilitiesAcceptanceModalFormProps,
  IHandleVulnerabilitiesAcceptanceModalProps,
  IHandleVulnerabilitiesAcceptanceResultAttr,
  IRejectZeroRiskVulnResultAttr,
  IRejectVulnerabilitiesResultAttr,
  IVulnDataAttr,
  IAcceptanceVulns,
  VulnUpdateResult,
};
