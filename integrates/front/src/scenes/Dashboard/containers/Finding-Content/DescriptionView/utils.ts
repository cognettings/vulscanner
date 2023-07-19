import yaml from "js-yaml";
import _ from "lodash";

import type {
  IUnfulfilledRequirement,
  IVulnerabilityCriteriaData,
  IVulnerabilityCriteriaRequirement,
} from "./types";

import { Logger } from "utils/logger";
import { translate } from "utils/translations/translate";

const BASE_URL: string =
  "https://gitlab.com/api/v4/projects/20741933/repository/files";
const BRANCH_REF: string = "trunk";
const REQUIREMENTS_FILE_ID: string =
  "common%2Fcriteria%2Fsrc%2Frequirements%2Fdata.yaml";

const formatFindingType: (type: string) => string = (type: string): string =>
  _.isEmpty(type)
    ? "-"
    : translate.t(`searchFindings.tabDescription.type.${type.toLowerCase()}`);

function formatRequirements(
  requirements: string[],
  criteriaData: Record<string, IVulnerabilityCriteriaRequirement> | undefined
): IUnfulfilledRequirement[] {
  if (criteriaData === undefined || _.isEmpty(requirements)) {
    return [];
  }
  const requirementsData: IUnfulfilledRequirement[] = requirements.map(
    (key: string): IUnfulfilledRequirement => {
      return { id: key, summary: criteriaData[key].en.summary };
    }
  );

  return requirementsData;
}

function getRequirementsText(
  requirements: string[],
  criteriaData: Record<string, IVulnerabilityCriteriaRequirement> | undefined,
  language?: string
): string[] {
  if (criteriaData === undefined || _.isEmpty(requirements)) {
    return requirements;
  }
  const requirementsSummaries: string[] = requirements.map(
    (key: string): string => {
      const summary =
        language === "ES"
          ? criteriaData[key].es.summary
          : criteriaData[key].en.summary;

      return `${key}. ${summary}`;
    }
  );

  return requirementsSummaries;
}

const getRequerimentsData = async (): Promise<
  Record<string, IVulnerabilityCriteriaRequirement> | undefined
> => {
  const requirementsResponseFile: Response = await fetch(
    `${BASE_URL}/${REQUIREMENTS_FILE_ID}/raw?ref=${BRANCH_REF}`
  );
  const requirementsYamlFile: string = await requirementsResponseFile.text();

  return requirementsYamlFile
    ? (yaml.load(requirementsYamlFile) as Record<
        string,
        IVulnerabilityCriteriaRequirement
      >)
    : undefined;
};

const getVulnerabilitiesCriteriaData = async (): Promise<
  Record<string, IVulnerabilityCriteriaData>
> => {
  const baseUrl: string =
    "https://gitlab.com/api/v4/projects/20741933/repository/files";
  const branchRef: string = "trunk";
  const vulnsFileId: string =
    "common%2Fcriteria%2Fsrc%2Fvulnerabilities%2Fdata.yaml";
  const vulnerabilitiesInfo: string = await fetch(
    `${baseUrl}/${vulnsFileId}/raw?ref=${branchRef}`
  )
    .then(async (response: Response): Promise<string> => response.text())
    .catch((error: Error): string => {
      Logger.error("Failed to fetch vulnerabilities info", error);

      return `{
        "000": {
          en: {
            title: "__empty__",
            description: "__empty__",
            impact: "__empty__",
            recommendation: "__empty__",
            threat: "__empty__",
          },
          es: {
            title: "__empty__",
            description: "__empty__",
            impact: "__empty__",
            recommendation: "__empty__",
            threat: "__empty__",
          },
          score: {
            base: {
              attack_vector: "__empty__",
              attack_complexity: "__empty__",
              privileges_required: "__empty__",
              user_interaction: "__empty__",
              scope: "__empty__",
              confidentiality: "__empty__",
              integrity: "__empty__",
              availability: "__empty__",
            },
            temporal: {
              exploit_code_maturity: "__empty__",
              remediation_level: "__empty__",
              report_confidence: "__empty__",
            },
          },
          remediation_time: "__empty__",
          requirements: ["__empty__"],
          metadata: {},
        }
      }`;
    });

  return yaml.load(vulnerabilitiesInfo) as Record<
    string,
    IVulnerabilityCriteriaData
  >;
};

// Empty fields in criteria's data.yaml are filled with "__empty__" or "X"
function validateNotEmpty(field: string | undefined): string {
  if (!_.isNil(field) && field !== "__empty__") {
    return field;
  }

  return "";
}

export {
  formatFindingType,
  formatRequirements,
  getRequerimentsData,
  getRequirementsText,
  getVulnerabilitiesCriteriaData,
  validateNotEmpty,
};
