interface IHeaderQueryResult {
  finding: {
    closedVulns: number;
    currentState: string;
    hacker?: string;
    id: string;
    maxOpenSeverityScore: number;
    minTimeToRemediate: number;
    openVulns: number;
    releaseDate: string | null;
    status: "SAFE" | "VULNERABLE";
    title: string;
    totalOpenCVSSF: number;
  };
}

interface IRemoveFindingResultAttr {
  removeFinding?: {
    success: boolean;
  };
}

export type { IHeaderQueryResult, IRemoveFindingResultAttr };
