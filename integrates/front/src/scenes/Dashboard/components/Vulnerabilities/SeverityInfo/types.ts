interface IVulnSeverityAttr {
  vulnerability: {
    id: string;
    severityTemporalScore: number;
    severityVector: string;
  };
}

interface IUpdateVulnsSeverityAttr {
  updateVulnerabilitiesSeverity: {
    success: boolean;
  };
}

export type { IVulnSeverityAttr, IUpdateVulnsSeverityAttr };
