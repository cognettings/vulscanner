interface IFilterSet {
  bePresent: string;
  component: string;
  hasVulnerabilities: string;
  rootId: string;
  seenAt: { max: string; min: string };
  seenFirstTimeBy: string;
}

interface IGroupToeInputsViewProps {
  isInternal: boolean;
}

interface IRemoveToeInputResultAttr {
  removeToeInput: {
    success: boolean;
  };
}

interface IToeInputEdge {
  node: IToeInputAttr;
}

interface IToeInputsConnection {
  edges: IToeInputEdge[];
  pageInfo: {
    hasNextPage: boolean;
    endCursor: string;
  };
}
interface IToeInputAttr {
  attackedAt: string | null;
  attackedBy: string;
  bePresent: boolean;
  bePresentUntil: string | null;
  component: string;
  entryPoint: string;
  firstAttackAt: string | null;
  hasVulnerabilities: boolean;
  root: IGitRootAttr | null;
  seenAt: string | null;
  seenFirstTimeBy: string;
}

interface IGitRootAttr {
  id: string;
  nickname: string;
}

interface IToeInputData {
  attackedAt: Date | undefined;
  attackedBy: string;
  bePresent: boolean;
  bePresentUntil: Date | undefined;
  component: string;
  entryPoint: string;
  firstAttackAt: Date | undefined;
  hasVulnerabilities: boolean;
  markedSeenFirstTimeBy: string;
  root: IGitRootAttr | null;
  rootId: string;
  rootNickname: string;
  seenAt: Date | undefined;
  seenFirstTimeBy: string;
}

interface IUpdateToeInputResultAttr {
  updateToeInput: {
    success: boolean;
    toeInput: IToeInputAttr | undefined;
  };
}

export type {
  IFilterSet,
  IGitRootAttr,
  IGroupToeInputsViewProps,
  IRemoveToeInputResultAttr,
  IToeInputAttr,
  IToeInputEdge,
  IToeInputData,
  IToeInputsConnection,
  IUpdateToeInputResultAttr,
};
