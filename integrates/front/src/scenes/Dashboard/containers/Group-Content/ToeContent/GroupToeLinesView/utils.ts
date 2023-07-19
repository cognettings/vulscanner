import _ from "lodash";

import type { IFilter } from "components/Filter";
import type {
  IToeLinesAttr,
  IToeLinesData,
  IToeLinesEdge,
} from "scenes/Dashboard/containers/Group-Content/ToeContent/GroupToeLinesView/types";

const NOEXTENSION = ".no.extension.";
const COMMIT_LENGTH = 7;

const formatBePresent = (bePresent: string): boolean | undefined =>
  bePresent === "" ? undefined : bePresent === "true";

const formatRootId = (rootId: string): string | undefined =>
  rootId === "" ? undefined : rootId;

const commitFormatter = (value: string): string =>
  value.slice(0, COMMIT_LENGTH);

const getCoverage = (toeLinesAttr: IToeLinesAttr): number =>
  toeLinesAttr.loc === 0 ? 1 : toeLinesAttr.attackedLines / toeLinesAttr.loc;

const getDaysToAttack = (toeLinesAttr: IToeLinesAttr): number => {
  if (
    _.isNull(toeLinesAttr.attackedAt) ||
    _.isEmpty(toeLinesAttr.attackedAt) ||
    new Date(toeLinesAttr.modifiedDate) > new Date(toeLinesAttr.attackedAt)
  ) {
    if (toeLinesAttr.bePresent) {
      return Math.floor(
        (new Date().getTime() - new Date(toeLinesAttr.modifiedDate).getTime()) /
          (1000 * 3600 * 24)
      );
    }

    return Math.floor(
      (new Date(toeLinesAttr.bePresentUntil ?? "").getTime() -
        new Date(toeLinesAttr.modifiedDate).getTime()) /
        (1000 * 3600 * 24)
    );
  }

  return Math.floor(
    (new Date(toeLinesAttr.attackedAt).getTime() -
      new Date(toeLinesAttr.modifiedDate).getTime()) /
      (1000 * 3600 * 24)
  );
};

const getExtension = (toeLinesAttr: IToeLinesAttr): string => {
  const lastPointindex = toeLinesAttr.filename.lastIndexOf(".");
  const lastSlashIndex = toeLinesAttr.filename.lastIndexOf("/");
  if (lastPointindex === -1 || lastSlashIndex > lastPointindex) {
    return NOEXTENSION;
  }

  return toeLinesAttr.filename.slice(lastPointindex + 1);
};

const formatOptionalDate: (date: string | null) => Date | undefined = (
  date: string | null
): Date | undefined =>
  _.isNull(date) || _.isEmpty(date) ? undefined : new Date(date);

const formatToeLines: (toeLinesEdges: IToeLinesEdge[]) => IToeLinesData[] = (
  toeLinesEdges: IToeLinesEdge[]
): IToeLinesData[] =>
  toeLinesEdges.map(
    ({ node }): IToeLinesData => ({
      ...node,
      attackedAt: formatOptionalDate(node.attackedAt),
      bePresentUntil: formatOptionalDate(node.bePresentUntil),
      coverage: getCoverage(node),
      daysToAttack: getDaysToAttack(node),
      extension: getExtension(node),
      firstAttackAt: formatOptionalDate(node.firstAttackAt),
      lastCommit: commitFormatter(node.lastCommit),
      modifiedDate: formatOptionalDate(node.modifiedDate),
      rootId: node.root.id,
      rootNickname: node.root.nickname,
      seenAt: formatOptionalDate(node.seenAt),
    })
  );

const formatLinesFilter: (state: string) => string[] | string = (
  state: string
): string[] | string => {
  const linesParameters: Record<string, string[] | string> = {
    attackedAt: ["fromAttackedAt", "toAttackedAt"],
    attackedBy: "attackedBy",
    attackedLines: ["minAttackedLines", "maxAttackedLines"],
    bePresent: "bePresent",
    bePresentUntil: ["fromBePresentUntil", "toBePresentUntil"],
    comments: "comments",
    coverage: ["minCoverage", "maxCoverage"],
    filename: "filename",
    firstAttackAt: ["fromFirstAttackAt", "toFirstAttackAt"],
    hasVulnerabilities: "hasVulnerabilities",
    lastAuthor: "lastAuthor",
    lastCommit: "lastCommit",
    loc: ["minLoc", "maxLoc"],
    modifiedDate: ["fromModifiedDate", "toModifiedDate"],
    seenAt: ["fromSeenAt", "toSeenAt"],
    sortsPriorityFactor: ["minSortsPriorityFactor", "maxSortsPriorityFactor"],
  };

  return linesParameters[state];
};

const unformatFilterValues: (
  value: IFilter<IToeLinesData>
) => Record<string, unknown> = (
  value: IFilter<IToeLinesData>
): Record<string, unknown> => {
  const unformat = (): Record<string, unknown> => {
    const titleFormat = formatLinesFilter(value.id);

    if (typeof titleFormat === "string")
      return _.isNil(value.value) || _.isEmpty(value.value)
        ? { [titleFormat]: undefined }
        : {
            [titleFormat]: ["true", "false"].includes(value.value)
              ? JSON.parse(value.value)
              : value.value,
          };

    if (titleFormat[0].startsWith("min"))
      return {
        [titleFormat[0]]: value.numberRangeValues?.[0],
        [titleFormat[1]]: value.numberRangeValues?.[1],
      };

    return {
      [titleFormat[0]]: value.rangeValues?.[0],
      [titleFormat[1]]: value.rangeValues?.[1],
    };
  };

  return unformat();
};

export { formatBePresent, formatRootId, formatToeLines, unformatFilterValues };
