import type {
  ICVSS3EnvironmentalMetrics,
  ICVSS3TemporalMetrics,
} from "utils/cvss";

interface IGroupFindingsAttr {
  group: {
    __typename: "Group";
    businessId: string;
    businessName: string;
    description: string;
    findings: IFindingAttr[];
    hasMachine: boolean;
    name: string;
    userRole: string;
  };
}

interface ITreatmentSummaryAttr {
  __typename: "TreatmentSummary";
  accepted: number;
  acceptedUndefined: number;
  inProgress: number;
  untreated: number;
}

interface IVerificationSummaryAttr {
  __typename: "VerificationSummary";
  onHold: number;
  requested: number;
  verified: number;
}

interface ILocationsInfoAttr {
  findingId: string;
  openVulnerabilities: number;
  closedVulnerabilities: number;
  locations: string | undefined;
  treatmentAssignmentEmails: Set<string>;
}

interface IFindingAttr {
  __typename: "Finding";
  age: number;
  closedVulnerabilities: number;
  closingPercentage: number;
  description: string;
  id: string;
  isExploitable: boolean;
  lastVulnerability: number;
  locationsInfo: ILocationsInfoAttr;
  maxOpenSeverityScore: number;
  minTimeToRemediate: number | null;
  name: string;
  openAge: number;
  openVulnerabilities: number;
  reattack: string;
  rejectedVulnerabilities: number | undefined;
  releaseDate: string | null;
  root: string | null;
  status: "DRAFT" | "SAFE" | "VULNERABLE";
  submittedVulnerabilities: number | undefined;
  title: string;
  totalOpenCVSSF: number;
  treatment: string;
  treatmentSummary: ITreatmentSummaryAttr;
  verificationSummary: IVerificationSummaryAttr;
  verified: boolean;
}

interface IVulnerability {
  findingId: string;
  id: string;
  state: string;
  treatmentAssigned: string | null;
  where: string;
}

interface IGroupVulnerabilities {
  group: {
    name: string;
    vulnerabilities: {
      edges: { node: IVulnerability }[];
      pageInfo: {
        endCursor: string;
        hasNextPage: boolean;
      };
    };
  };
}

interface IVulnerabilitiesResume {
  treatmentAssignmentEmails: Set<string>;
  wheres: string;
}

interface IRoot {
  nickname: string;
  state: "ACTIVE" | "INACTIVE";
}

interface IFindingSuggestionData extends ICVSS3TemporalMetrics {
  attackVectorDescription: string;
  code: string;
  description: string;
  recommendation: string;
  minTimeToRemediate: number | null;
  threat: string;
  title: string;
  unfulfilledRequirements: string[];
}

interface IAddFindingFormValues extends ICVSS3EnvironmentalMetrics {
  description: string;
  threat: string;
  title: string;
}

interface IAddFindingMutationResult {
  addFinding: {
    success: boolean;
  };
}

export type {
  IAddFindingFormValues,
  IAddFindingMutationResult,
  IFindingAttr,
  IFindingSuggestionData,
  IGroupFindingsAttr,
  IGroupVulnerabilities,
  ILocationsInfoAttr,
  IRoot,
  ITreatmentSummaryAttr,
  IVerificationSummaryAttr,
  IVulnerabilitiesResume,
  IVulnerability,
};
