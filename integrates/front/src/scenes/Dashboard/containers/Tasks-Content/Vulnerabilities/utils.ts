import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { getNonSelectableVulnerabilitiesOnReattackIds } from "scenes/Dashboard/components/Vulnerabilities/utils";
import type {
  IGetUserOrganizationsGroups,
  IOrganizationGroups,
} from "scenes/Dashboard/types";

const filteredContinuousVulnerabilitiesOnReattackIds = (
  vulnerabilities: IVulnRowAttr[],
  groups: IOrganizationGroups["groups"]
): string[] => {
  const firstFilteredVulnerabilities =
    getNonSelectableVulnerabilitiesOnReattackIds(vulnerabilities);

  return vulnerabilities.reduce(
    (
      nonSelectableVulnerabilities: string[],
      vulnerability: IVulnRowAttr
    ): string[] => {
      const filteredGroups = groups.filter(
        (group): boolean =>
          group.name.toLowerCase() === vulnerability.groupName.toLowerCase()
      );

      if (filteredGroups.length === 0) {
        return nonSelectableVulnerabilities;
      }

      return filteredGroups[0].serviceAttributes.includes("is_continuous") &&
        !firstFilteredVulnerabilities.includes(vulnerability.id)
        ? [...nonSelectableVulnerabilities, vulnerability.id]
        : nonSelectableVulnerabilities;
    },
    []
  );
};

const getUserGroups = (
  userData: IGetUserOrganizationsGroups | undefined
): IOrganizationGroups["groups"] =>
  userData === undefined
    ? []
    : userData.me.organizations.reduce(
        (
          previousValue: IOrganizationGroups["groups"],
          currentValue
        ): IOrganizationGroups["groups"] => [
          ...previousValue,
          ...currentValue.groups,
        ],
        []
      );

export { filteredContinuousVulnerabilitiesOnReattackIds, getUserGroups };
