import type { IVulnRowAttr } from "../types";

interface IAdditionalInfoProps {
  canRetrieveHacker: boolean;
  canSeeSource: boolean;
  refetchData: () => void;
  vulnerability: IVulnRowAttr;
}

interface IFormValues {
  commitHash: string | null;
  source: string;
  type: string;
}

interface IGetVulnAdditionalInfoAttr {
  vulnerability: IVulnInfoAttr;
}

interface IUpdateVulnerabilityDescriptionAttr {
  updateVulnerabilityDescription: {
    success: boolean;
  };
}

interface IVulnerabilityAdvisories {
  cve: string[];
  package: string;
  vulnerableVersion: string;
}

interface IVulnInfoAttr {
  advisories: IVulnerabilityAdvisories | undefined;
  closingDate: string | null;
  commitHash: string | null;
  cycles: string;
  efficacy: string;
  hacker?: string;
  lastReattackRequester: string;
  lastRequestedReattackDate: string | null;
  lastStateDate: string;
  lastTreatmentDate: string;
  reportDate: string | null;
  rootNickname: string | null;
  severity: string | null;
  severityTemporalScore: number;
  severityVector: string;
  source: string;
  specific: string;
  stream: string | null;
  technique: string;
  treatmentStatus: string;
  treatmentAcceptanceStatus: string | null;
  treatmentAcceptanceDate: string | null;
  treatmentAssigned: string | null;
  treatmentChanges: string;
  treatmentJustification: string | null;
  vulnerabilityType: string;
  where: string;
}

export type {
  IAdditionalInfoProps,
  IFormValues,
  IGetVulnAdditionalInfoAttr,
  IUpdateVulnerabilityDescriptionAttr,
  IVulnInfoAttr,
};
