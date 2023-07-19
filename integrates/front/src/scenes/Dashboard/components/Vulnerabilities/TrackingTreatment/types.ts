import type { IHistoricTreatment } from "scenes/Dashboard/containers/Finding-Content/DescriptionView/types";

interface IHistoricTreatmentEdge {
  node: IHistoricTreatment;
}
interface IVulnHistoricTreatmentConnection {
  edges: IHistoricTreatmentEdge[];
  pageInfo: {
    hasNextPage: boolean;
    endCursor: string;
  };
}

interface IVulnTreatmentAttr {
  __typename: string;
  historicTreatmentConnection: IVulnHistoricTreatmentConnection;
  id: string;
}

interface IGetVulnTreatmentAttr {
  vulnerability: IVulnTreatmentAttr;
}

export type { IGetVulnTreatmentAttr, IHistoricTreatmentEdge };
