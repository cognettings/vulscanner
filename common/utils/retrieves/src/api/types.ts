import type {
  IGitRoot,
  IOrganization,
  IToeLines,
  IVulnerability,
} from "@retrieves/types";

interface IGetGitRoot {
  data: { root: IGitRoot };
}

interface IGetGitRoots {
  data: { group: { roots: IGitRoot[] } };
}

interface IGetGroups {
  data: {
    me: {
      organizations: IOrganization[];
    };
  };
}

interface IGetVulnerabilities {
  data: { root: { vulnerabilities: IVulnerability[] } };
}

interface IToeLinesEdge {
  node: IToeLines;
}

interface IToeLinesPaginator {
  edges: IToeLinesEdge[];
  pageInfo: {
    hasNextPage: boolean;
    endCursor: string;
  };
}

interface IToeLinesQuery {
  group: { toeLines: IToeLinesPaginator };
}

interface IUpdateAttackedFile {
  data: {
    updateToeLinesAttackedLines: { success: boolean; message?: string };
  };
}

export type {
  IGetGroups,
  IGetGitRoot,
  IGetGitRoots,
  IGetVulnerabilities,
  IToeLinesPaginator,
  IToeLinesQuery,
  IToeLinesEdge,
  IUpdateAttackedFile,
};
