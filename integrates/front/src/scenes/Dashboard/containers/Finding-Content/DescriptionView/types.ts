interface IHistoricTreatment {
  acceptanceDate?: string;
  acceptanceStatus?: string;
  date: string;
  justification?: string;
  treatment: string;
  assigned?: string;
  user: string;
}

interface IUnfulfilledRequirement {
  id: string;
  summary: string;
}

interface IFinding {
  attackVectorDescription: string;
  description: string;
  hacker?: string;
  id: string;
  openVulnerabilities: number;
  recommendation: string;
  releaseDate: string | null;
  sorts: string;
  status: "SAFE" | "VULNERABLE";
  threat: string;
  title: string;
  unfulfilledRequirements: IUnfulfilledRequirement[];
}

interface IFindingDescriptionData {
  finding: IFinding;
}

interface IFindingDescriptionVars {
  canRetrieveHacker: boolean;
  canRetrieveSorts: boolean;
  findingId: string;
}

interface ILanguageData {
  group: {
    language: string;
  };
}

interface IVulnerabilityLanguage {
  title: string;
  description: string;
  impact: string;
  recommendation: string;
  threat: string;
}

interface IVulnerabilityScore {
  base: {
    attack_vector: string;
    attack_complexity: string;
    privileges_required: string;
    user_interaction: string;
    scope: string;
    confidentiality: string;
    integrity: string;
    availability: string;
  };
  temporal: {
    exploit_code_maturity: string;
    remediation_level: string;
    report_confidence: string;
  };
}

interface IVulnerabilityCriteriaData {
  en: IVulnerabilityLanguage;
  es: IVulnerabilityLanguage;
  score: IVulnerabilityScore;
  remediation_time: string;
  requirements: string[];
  metadata: Record<string, unknown>;
}

interface IVulnerabilityCriteriaLanguage {
  title: string;
  summary: string;
  description: string;
}

interface IVulnerabilityCriteriaRequirement {
  en: IVulnerabilityCriteriaLanguage;
  es: IVulnerabilityCriteriaLanguage;
  category: string;
  references: string;
  metadata: Record<string, unknown>;
}

export type {
  IHistoricTreatment,
  IFinding,
  IFindingDescriptionData,
  IFindingDescriptionVars,
  ILanguageData,
  IUnfulfilledRequirement,
  IVulnerabilityCriteriaData,
  IVulnerabilityCriteriaRequirement,
};
