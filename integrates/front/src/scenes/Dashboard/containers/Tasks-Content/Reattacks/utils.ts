import _ from "lodash";

import { getOrganizationGroups } from "scenes/Dashboard/components/Vulnerabilities/utils";
import type {
  IFindingFormatted,
  IFindingToReattackEdge,
  ITodoFindingToReattackAttr,
  IVulnerabilityEdge,
} from "scenes/Dashboard/containers/Tasks-Content/Reattacks/types";
import type { IOrganizationGroups } from "scenes/Dashboard/types";

const getOldestRequestedReattackDate = (
  edges: IVulnerabilityEdge[]
): string => {
  const vulnsDates: string[] = edges.map(
    (vulnEdge: IVulnerabilityEdge): string =>
      vulnEdge.node.lastRequestedReattackDate
  );
  const minDate = _.min(vulnsDates);
  if (_.isUndefined(minDate)) {
    return "-";
  }

  return minDate;
};

const noDate = (finding: IFindingFormatted): IFindingFormatted | undefined => {
  return finding.oldestReattackRequestedDate === "-" ? undefined : finding;
};

const formatFindings = (
  organizationsGroups: IOrganizationGroups[] | undefined,
  findings: IFindingToReattackEdge[]
): IFindingFormatted[] => {
  const formatted = findings
    .map((edge): ITodoFindingToReattackAttr => edge.node)
    .map((finding): IFindingFormatted => {
      const organizationGroups: IOrganizationGroups | undefined =
        getOrganizationGroups(organizationsGroups, finding.groupName);

      const organizationName: string =
        organizationGroups === undefined ? "" : organizationGroups.name;

      return {
        ...finding,
        oldestReattackRequestedDate: getOldestRequestedReattackDate(
          finding.vulnerabilitiesToReattackConnection.edges
        ),
        organizationName,
        url: `https://app.fluidattacks.com/orgs/${organizationName}/groups/${finding.groupName}/vulns/${finding.id}/locations`,
      };
    });

  const fmtd = formatted.filter(noDate);

  return _.orderBy(fmtd, ["oldestReattackRequestedDate"], ["asc"]);
};

export { formatFindings };
