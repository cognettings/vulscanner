import type { IVulnRowAttr as IVulnerabilityAttr } from "scenes/Dashboard/components/Vulnerabilities/types";

interface IFinding {
  id: string;
  title: string;
}

interface IGroupVulnerabilities {
  group: {
    name: string;
    vulnerabilities: {
      edges: { node: IVulnerabilityAttr }[];
      pageInfo: {
        endCursor: string;
        hasNextPage: boolean;
      };
      total: number | undefined;
    };
  };
}

interface IGroupVulnerabilityDrafts {
  group: {
    name: string;
    vulnerabilityDrafts:
      | {
          edges: { node: IVulnerabilityAttr }[];
          pageInfo: {
            endCursor: string;
            hasNextPage: boolean;
          };
          total: number | undefined;
        }
      | undefined;
  };
}

export type { IFinding, IGroupVulnerabilities, IGroupVulnerabilityDrafts };
