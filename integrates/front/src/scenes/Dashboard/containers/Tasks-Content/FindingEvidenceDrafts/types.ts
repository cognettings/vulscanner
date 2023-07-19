interface IFinding {
  groupName: string;
  id: string;
  title: string;
}

interface IFindingEvidenceDrafts {
  me: {
    findingEvidenceDrafts: {
      edges: { node: IFinding }[];
      pageInfo: {
        endCursor: string;
        hasNextPage: boolean;
      };
      total: number | undefined;
    };
    userEmail: string;
  };
}

export type { IFinding, IFindingEvidenceDrafts };
