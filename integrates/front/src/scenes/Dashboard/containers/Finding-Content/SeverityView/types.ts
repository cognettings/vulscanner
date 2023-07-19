import type { ICVSS3EnvironmentalMetrics } from "utils/cvss";

interface ISeverityAttr {
  finding: {
    cvssVersion: string;
    id: string;
    severity: ICVSS3EnvironmentalMetrics;
    severityVector: string;
  };
}

interface IUpdateSeverityAttr {
  updateSeverity: {
    success: boolean;
  };
}

interface ISeverityField {
  currentValue: string;
  name: string;
  options: Record<string, string>;
  title: string;
}

export type { ISeverityAttr, IUpdateSeverityAttr, ISeverityField };
