/* eslint @typescript-eslint/strict-boolean-expressions:0 */
/* eslint @typescript-eslint/no-unnecessary-condition:0 */
import dayjs from "dayjs";
import _ from "lodash";

import type {
  IFormatVulns,
  IFormatVulnsTreatment,
  IGetVulnById,
  IVulnRowAttr,
  vulnerabilityStatesStrings,
} from "scenes/Dashboard/components/Vulnerabilities/types";
import { vulnerabilityStates } from "scenes/Dashboard/components/Vulnerabilities/types";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/Finding-Content/DescriptionView/types";
import { getRequirementsText } from "scenes/Dashboard/containers/Finding-Content/DescriptionView/utils";
import type { IReqFormat } from "scenes/Dashboard/containers/Group-Content/GroupVulnerabilitiesView/formatters/types";
import type { IGroups, IOrganizationGroups } from "scenes/Dashboard/types";
import { isWithInAWeek } from "utils/date";
import { formatDropdownField } from "utils/formatHelpers";
import { translate } from "utils/translations/translate";

const CRITERIA_ID_SLICE: number = 3;
const EMPTY_STRING: string = "";
const DASH_STRING: string = "-";

const requirementsTitle = ({
  findingTitle,
  requirementsData,
  vulnsData,
}: IReqFormat): string[] => {
  const findingNumber =
    !_.isNil(findingTitle) && findingTitle
      ? findingTitle.slice(0, CRITERIA_ID_SLICE)
      : EMPTY_STRING;

  if (!_.isNil(vulnsData) && !_.isNil(findingNumber)) {
    const { requirements } = vulnsData[findingNumber] || [];

    return getRequirementsText(requirements, requirementsData);
  }

  return [];
};

const formatTreatment = (
  treatmentStatus: string,
  state: vulnerabilityStatesStrings,
  treatmentAcceptanceStatus: string | null
): string => {
  const isPendingToApproval: boolean =
    treatmentStatus === "ACCEPTED_UNDEFINED" &&
    treatmentAcceptanceStatus !== "APPROVED";
  const isVulnOpen: boolean = state === vulnerabilityStates.VULNERABLE;
  const pendingApproval: string = isPendingToApproval
    ? translate.t("searchFindings.tabDescription.treatment.pendingApproval")
    : EMPTY_STRING;
  const treatmentLabel: string =
    translate.t(formatDropdownField(treatmentStatus)) + pendingApproval;

  return isVulnOpen ? treatmentLabel : DASH_STRING;
};

const formatVulnerabilities: ({
  requirementsData,
  vulnerabilities,
  vulnsData,
}: IFormatVulns) => IVulnRowAttr[] = ({
  requirementsData,
  vulnerabilities,
  vulnsData,
}): IVulnRowAttr[] =>
  vulnerabilities.map((vulnerability: IVulnRowAttr): IVulnRowAttr => {
    const isVulnOpen: boolean =
      vulnerability.state === vulnerabilityStates.VULNERABLE;
    const verification: string =
      vulnerability.verification === "Verified"
        ? `${vulnerability.verification} (${vulnerability.state.toLowerCase()})`
        : (vulnerability.verification as string);
    const isLastVerificationWithInAWeek: boolean = Boolean(
      isWithInAWeek(
        dayjs(vulnerability.lastVerificationDate, "YYYY-MM-DD hh:mm:ss")
      )
    );
    const isVulnVerified: boolean =
      !_.isEmpty(vulnerability.lastVerificationDate) &&
      vulnerability.verification === "Verified";
    const shouldDisplayVerification: boolean = isVulnVerified
      ? isLastVerificationWithInAWeek
      : true;
    const requirements: string[] = requirementsTitle({
      findingTitle: vulnerability.finding?.title,
      requirementsData,
      vulnsData,
    });

    const formatDate = (date: string | null | undefined): string => {
      return _.isNil(date) ? DASH_STRING : date.split(" ")[0];
    };

    return {
      ...vulnerability,
      assigned: isVulnOpen
        ? (vulnerability.treatmentAssigned as string)
        : DASH_STRING,
      lastStateDate: formatDate(vulnerability.lastStateDate),
      lastTreatmentDate: isVulnOpen
        ? formatDate(vulnerability.lastTreatmentDate)
        : DASH_STRING,
      reportDate: _.isNull(vulnerability.reportDate)
        ? DASH_STRING
        : formatDate(vulnerability.reportDate),
      requirements,
      treatmentAssigned: isVulnOpen
        ? (vulnerability.treatmentAssigned as string)
        : DASH_STRING,
      treatmentDate: isVulnOpen
        ? formatDate(vulnerability.lastTreatmentDate)
        : DASH_STRING,
      treatmentStatus: formatTreatment(
        vulnerability.treatmentStatus,
        vulnerability.state,
        vulnerability.treatmentAcceptanceStatus
      ),
      treatmentUser: isVulnOpen
        ? (vulnerability.treatmentUser as string)
        : DASH_STRING,
      verification: shouldDisplayVerification ? verification : EMPTY_STRING,
      vulnerabilityType: translate.t(
        `searchFindings.tabVuln.vulnTable.vulnerabilityType.${vulnerability.vulnerabilityType}`
      ),
    };
  });

const formatHistoricTreatment: (
  vulnerabilities: IVulnRowAttr
) => IHistoricTreatment = (vulnerability: IVulnRowAttr): IHistoricTreatment => {
  return {
    acceptanceDate: _.isNull(vulnerability.treatmentAcceptanceDate)
      ? undefined
      : vulnerability.treatmentAcceptanceDate,
    acceptanceStatus: _.isNull(vulnerability.treatmentAcceptanceStatus)
      ? undefined
      : vulnerability.treatmentAcceptanceStatus,
    assigned: _.isNull(vulnerability.treatmentAssigned)
      ? undefined
      : vulnerability.treatmentAssigned,
    date: vulnerability.lastTreatmentDate,
    justification: _.isNull(vulnerability.treatmentJustification)
      ? undefined
      : vulnerability.treatmentJustification,
    treatment: vulnerability.treatmentStatus,
    user: _.isNull(vulnerability.treatmentUser)
      ? EMPTY_STRING
      : vulnerability.treatmentUser,
  };
};

const getOrganizationGroups = (
  organizationsGroups: IOrganizationGroups[] | undefined,
  groupName: string
): IOrganizationGroups | undefined => {
  const organizationGroups: IOrganizationGroups | undefined =
    organizationsGroups?.find(
      (orgGroup: IOrganizationGroups): boolean =>
        orgGroup.groups.find(
          (group: IGroups): boolean => group.name === groupName
        )?.name === groupName
    );

  return organizationGroups;
};

const formatVulnerabilitiesTreatment = ({
  organizationsGroups,
  vulnerabilities,
}: IFormatVulnsTreatment): IVulnRowAttr[] =>
  vulnerabilities.map((vulnerability: IVulnRowAttr): IVulnRowAttr => {
    const lastTreatment: IHistoricTreatment =
      formatHistoricTreatment(vulnerability);
    const organizationGroups: IOrganizationGroups | undefined =
      getOrganizationGroups(organizationsGroups, vulnerability.groupName);

    return {
      ...vulnerability,
      historicTreatment: [lastTreatment],
      organizationName:
        organizationGroups === undefined
          ? EMPTY_STRING
          : organizationGroups.name,
    };
  });

function filterZeroRisk(vulnerabilities: IVulnRowAttr[]): IVulnRowAttr[] {
  return vulnerabilities.filter(
    (vuln: IVulnRowAttr): boolean =>
      _.isEmpty(vuln.zeroRisk) || vuln.zeroRisk === "Rejected"
  );
}

function getNonSelectableVulnerabilitiesOnReattackIds(
  vulnerabilities: IVulnRowAttr[]
): string[] {
  return vulnerabilities.reduce(
    (
      nonSelectableVulnerabilities: string[],
      vulnerability: IVulnRowAttr
    ): string[] => {
      const isVulnNonSelectable: boolean =
        vulnerability.remediated ||
        vulnerability.state === vulnerabilityStates.REJECTED ||
        vulnerability.state === vulnerabilityStates.SAFE ||
        vulnerability.state === vulnerabilityStates.SUBMITTED ||
        vulnerability.verification?.toLowerCase() === "on_hold";

      return isVulnNonSelectable
        ? [...nonSelectableVulnerabilities, vulnerability.id]
        : nonSelectableVulnerabilities;
    },
    []
  );
}

function getNonSelectableVulnerabilitiesOnVerifyIds(
  vulnerabilities: IVulnRowAttr[]
): string[] {
  return vulnerabilities.reduce(
    (
      nonSelectableVulnerabilities: string[],
      vulnerability: IVulnRowAttr
    ): string[] =>
      vulnerability.remediated &&
      vulnerability.state === vulnerabilityStates.VULNERABLE
        ? nonSelectableVulnerabilities
        : [...nonSelectableVulnerabilities, vulnerability.id],
    []
  );
}

function getNonSelectableVulnerabilitiesOnCloseIds(
  vulnerabilities: IVulnRowAttr[]
): string[] {
  return vulnerabilities.reduce(
    (
      nonSelectableVulnerabilities: string[],
      vulnerability: IVulnRowAttr
    ): string[] =>
      vulnerability.state === vulnerabilityStates.VULNERABLE
        ? nonSelectableVulnerabilities
        : [...nonSelectableVulnerabilities, vulnerability.id],
    []
  );
}

function getNonSelectableVulnerabilitiesOnResubmitIds(
  vulnerabilities: IVulnRowAttr[]
): string[] {
  return vulnerabilities.reduce(
    (
      nonSelectableVulnerabilities: string[],
      vulnerability: IVulnRowAttr
    ): string[] =>
      vulnerability.state === vulnerabilityStates.REJECTED
        ? nonSelectableVulnerabilities
        : [...nonSelectableVulnerabilities, vulnerability.id],
    []
  );
}

function filterOutVulnerabilities(
  selectedVulnerabilities: IVulnRowAttr[],
  allVulnerabilities: IVulnRowAttr[],
  filter: (vulnerabilities: IVulnRowAttr[]) => string[]
): IVulnRowAttr[] {
  return Array.from(
    new Set(
      selectedVulnerabilities.filter(
        (selectedVulnerability: IVulnRowAttr): boolean =>
          !filter(allVulnerabilities).includes(selectedVulnerability.id)
      )
    )
  );
}

const getVulnerabilityById: ({
  vulnerabilities,
  vulnerabilityId,
}: IGetVulnById) => IVulnRowAttr | undefined = ({
  vulnerabilities,
  vulnerabilityId,
}): IVulnRowAttr | undefined => {
  const vulns = vulnerabilities.filter(
    (vulnerability: IVulnRowAttr): boolean =>
      vulnerability.id === vulnerabilityId
  );

  return vulns.length > 0 ? vulns[0] : undefined;
};

export {
  filterOutVulnerabilities,
  filterZeroRisk,
  formatHistoricTreatment,
  formatVulnerabilities,
  formatVulnerabilitiesTreatment,
  getNonSelectableVulnerabilitiesOnCloseIds,
  getNonSelectableVulnerabilitiesOnReattackIds,
  getNonSelectableVulnerabilitiesOnResubmitIds,
  getNonSelectableVulnerabilitiesOnVerifyIds,
  getOrganizationGroups,
  getVulnerabilityById,
  formatTreatment,
};
