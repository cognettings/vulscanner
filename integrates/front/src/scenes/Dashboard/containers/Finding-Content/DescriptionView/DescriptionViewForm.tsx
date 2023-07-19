import { Form, useFormikContext } from "formik";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { Fragment, useCallback, useEffect, useState } from "react";
import type { ReactElement } from "react";
import { useTranslation } from "react-i18next";
import type { ConfigurableValidator } from "revalidate";

import {
  formatRequirements,
  getRequerimentsData,
  getVulnerabilitiesCriteriaData,
  validateNotEmpty,
} from "./utils";

import { ExternalLink } from "components/ExternalLink";
import {
  Checkbox,
  Editable,
  Input,
  Label,
  Select,
  TextArea,
} from "components/Input";
import { FormGroup } from "components/Input/styles";
import { Col, Row } from "components/Layout";
import { Tooltip } from "components/Tooltip";
import { Can } from "context/authz/Can";
import { Have } from "context/authz/Have";
import { ActionButtons } from "scenes/Dashboard/containers/Finding-Content/DescriptionView/ActionButtons";
import type {
  IFinding,
  IFindingDescriptionData,
  IUnfulfilledRequirement,
  IVulnerabilityCriteriaData,
} from "scenes/Dashboard/containers/Finding-Content/DescriptionView/types";
import {
  composeValidators,
  maxLength,
  required,
  validDraftTitle,
  validFindingTypology,
  validTextField,
} from "utils/validations";

const MAX_DESCRIPTION_LENGTH = 1000;
const MAX_IMPACTS_LENGTH = 650;
const MAX_THREAT_LENGTH = 650;
const MAX_RECOMENDATION_LENGTH = 500;
const maxDescriptionLength: ConfigurableValidator = maxLength(
  MAX_DESCRIPTION_LENGTH
);
const maxImpactsLength: ConfigurableValidator = maxLength(MAX_IMPACTS_LENGTH);
const maxThreatLength: ConfigurableValidator = maxLength(MAX_THREAT_LENGTH);
const maxRecommendationLength: ConfigurableValidator = maxLength(
  MAX_RECOMENDATION_LENGTH
);

interface IDescriptionViewFormProps {
  data: IFindingDescriptionData;
  isDraft: boolean;
  isEditing: boolean;
  groupLanguage: string | undefined;
  setEditing: React.Dispatch<React.SetStateAction<boolean>>;
}

const DescriptionViewForm: React.FC<IDescriptionViewFormProps> = ({
  data,
  isDraft,
  isEditing,
  groupLanguage,
  setEditing,
}: IDescriptionViewFormProps): JSX.Element => {
  const { dirty, resetForm, submitForm, setValues, values, initialValues } =
    useFormikContext<IFinding & { requirementIds: string[] }>();
  const { t } = useTranslation();

  const isDescriptionPristine = !dirty;

  const criteriaIdSlice: number = 3;
  const findingNumber = values.title.slice(0, criteriaIdSlice);
  const baseCriteriaUrl: string = "https://docs.fluidattacks.com/criteria/";

  const [titleSuggestions, setTitleSuggestions] = useState<string[]>([]);

  const [criteriaBaseRequirements, setCriteriaBaseRequirements] = useState<
    IUnfulfilledRequirement[] | undefined
  >(undefined);
  const [criteriaVulnerabilityData, setCriteriaVulnerabilityData] = useState<
    Record<string, IVulnerabilityCriteriaData> | undefined
  >(undefined);

  const toggleEdit: () => void = useCallback((): void => {
    if (!isDescriptionPristine) {
      resetForm();
    }
    setEditing(!isEditing);
  }, [isDescriptionPristine, isEditing, resetForm, setEditing]);

  const handleSubmit: () => void = useCallback((): void => {
    if (!isDescriptionPristine) {
      void submitForm();
    }
  }, [isDescriptionPristine, submitForm]);

  const track = useCallback(
    (url: string): (() => void) =>
      (): void => {
        mixpanel.track("VulnerabilityLink", { url });
      },
    []
  );

  useEffect((): void => {
    async function fetchData(): Promise<void> {
      if (_.isUndefined(criteriaVulnerabilityData)) {
        const vulnsData = await getVulnerabilitiesCriteriaData();
        setCriteriaVulnerabilityData(vulnsData);

        if (!_.isNil(vulnsData) && !_.isNil(findingNumber)) {
          const titlesList = Object.keys(vulnsData).map(
            (key: string): string => {
              return groupLanguage === "ES"
                ? `${key}. ${validateNotEmpty(vulnsData[key].es.title)}`
                : `${key}. ${validateNotEmpty(vulnsData[key].en.title)}`;
            }
          );
          setTitleSuggestions(titlesList);
        }
      }
    }
    void fetchData();
  }, [
    criteriaVulnerabilityData,
    findingNumber,
    groupLanguage,
    setCriteriaBaseRequirements,
  ]);
  useEffect((): void => {
    async function fetchData(): Promise<void> {
      if (
        isEditing &&
        !_.isUndefined(criteriaVulnerabilityData) &&
        !_.isEmpty(findingNumber)
      ) {
        const EMPTY_REQUIREMENTS = { requirements: [] };
        const { requirements } = _.isUndefined(
          criteriaVulnerabilityData[findingNumber]
        )
          ? EMPTY_REQUIREMENTS
          : criteriaVulnerabilityData[findingNumber];
        const requirementsData = await getRequerimentsData();
        setCriteriaBaseRequirements(
          formatRequirements(requirements, requirementsData)
        );
        // eslint-disable-next-line @typescript-eslint/prefer-string-starts-ends-with
        if (data.finding.title.slice(0, criteriaIdSlice) === findingNumber) {
          setValues({
            ...values,
            requirementIds: initialValues.requirementIds,
          });
        } else {
          setValues({ ...values, requirementIds: requirements });
        }
      }
    }
    void fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [
    criteriaVulnerabilityData,
    data.finding.title,
    findingNumber,
    isEditing,
    setValues,
  ]);

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const dataset: IFinding = data.finding;

  const validateFindingTypology: ConfigurableValidator =
    validFindingTypology(titleSuggestions);

  return (
    <Form data-private={true} id={"editDescription"}>
      <Have I={"can_report_vulnerabilities"}>
        <ActionButtons
          isEditing={isEditing}
          isPristine={isDescriptionPristine}
          onEdit={toggleEdit}
          onUpdate={handleSubmit}
        />
      </Have>
      <br />
      <div>
        <div>
          <Row>
            <Can do={"api_resolvers_finding_hacker_resolve"}>
              <Col lg={45} md={45} sm={45}>
                <FormGroup>
                  <Label>
                    <b>{t("searchFindings.tabDescription.hacker")}</b>
                  </Label>
                  <p className={"ma0"}>{dataset.hacker}</p>
                </FormGroup>
              </Col>
            </Can>
          </Row>
          <Can do={"api_mutations_update_finding_description_mutate"}>
            {isEditing && isDraft ? (
              <Row>
                <Col>
                  <Tooltip
                    id={"searchFindings.tabDescription.title.tooltip"}
                    tip={t("searchFindings.tabDescription.title.tooltip")}
                  >
                    <FormGroup>
                      <Input
                        label={t("searchFindings.tabDescription.title.text")}
                        list={"title-list"}
                        name={"title"}
                        suggestions={_.sortBy(titleSuggestions)}
                        validate={composeValidators([
                          required,
                          validDraftTitle,
                          validateFindingTypology,
                        ])}
                      />
                    </FormGroup>
                  </Tooltip>
                </Col>
              </Row>
            ) : undefined}
          </Can>
          <Row>
            <Can
              do={"api_mutations_update_finding_description_mutate"}
              passThrough={true}
            >
              {(canEdit: boolean): JSX.Element => (
                <Col>
                  <Editable
                    currentValue={dataset.description}
                    isEditing={isEditing && canEdit}
                    label={t("searchFindings.tabDescription.description.text")}
                    tooltip={t(
                      "searchFindings.tabDescription.description.tooltip"
                    )}
                  >
                    <TextArea
                      id={"searchFindings.tabDescription.description.tooltip"}
                      label={t(
                        "searchFindings.tabDescription.description.text"
                      )}
                      name={"description"}
                      tooltip={t(
                        "searchFindings.tabDescription.description.tooltip"
                      )}
                      validate={composeValidators([
                        required,
                        validTextField,
                        maxDescriptionLength,
                      ])}
                    />
                  </Editable>
                  {isEditing && canEdit ? undefined : (
                    <ExternalLink
                      href={`${baseCriteriaUrl}vulnerabilities/${findingNumber}`}
                      onClick={track(
                        `${baseCriteriaUrl}vulnerabilities/${findingNumber}`
                      )}
                    >
                      {t(
                        "searchFindings.tabDescription.description.infoLinkText"
                      )}
                    </ExternalLink>
                  )}
                </Col>
              )}
            </Can>
          </Row>
          <br />
          <Row>
            <Col>
              <Tooltip
                id={"searchFindings.tabDescription.requirements.tooltip.id"}
                tip={t("searchFindings.tabDescription.requirements.tooltip")}
              >
                <FormGroup>
                  <Label>
                    <b>
                      {t("searchFindings.tabDescription.requirements.text")}
                    </b>
                  </Label>
                  <Can
                    do={"api_mutations_update_finding_description_mutate"}
                    passThrough={true}
                  >
                    {(canEdit: boolean): JSX.Element =>
                      isEditing && canEdit ? (
                        <Fragment>
                          {_.defaultTo(criteriaBaseRequirements, []).map(
                            (
                              requirement: IUnfulfilledRequirement
                            ): ReactElement => (
                              <Checkbox
                                id={requirement.id}
                                key={`requirementIds.${requirement.id}`}
                                label={t(
                                  `${requirement.id}. ${requirement.summary}`
                                )}
                                name={"requirementIds"}
                                value={requirement.id}
                              />
                            )
                          )}
                        </Fragment>
                      ) : (
                        <div className={"ws-pre-wrap"}>
                          {dataset.unfulfilledRequirements.map(
                            (
                              requirement: IUnfulfilledRequirement
                            ): ReactElement => {
                              return (
                                <div className={"w-100"} key={requirement.id}>
                                  <ExternalLink
                                    href={`${baseCriteriaUrl}requirements/${requirement.id}`}
                                    onClick={track(
                                      `${baseCriteriaUrl}requirements/${requirement.id}`
                                    )}
                                  >
                                    {`${requirement.id}. ${requirement.summary}`}
                                  </ExternalLink>
                                </div>
                              );
                            }
                          )}
                        </div>
                      )
                    }
                  </Can>
                </FormGroup>
              </Tooltip>
            </Col>
          </Row>
          <Row>
            <Col lg={45} md={45} sm={45}>
              <Can
                do={"api_mutations_update_finding_description_mutate"}
                passThrough={true}
              >
                {(canEdit: boolean): JSX.Element => (
                  <Editable
                    currentValue={dataset.attackVectorDescription}
                    isEditing={isEditing && canEdit}
                    label={t(
                      "searchFindings.tabDescription.attackVectors.text"
                    )}
                    tooltip={t(
                      "searchFindings.tabDescription.attackVectors.tooltip"
                    )}
                  >
                    <TextArea
                      id={"searchFindings.tabDescription.attackVectors.tooltip"}
                      label={t(
                        "searchFindings.tabDescription.attackVectors.text"
                      )}
                      name={"attackVectorDescription"}
                      tooltip={t(
                        "searchFindings.tabDescription.attackVectors.tooltip"
                      )}
                      validate={composeValidators([
                        required,
                        validTextField,
                        maxImpactsLength,
                      ])}
                    />
                  </Editable>
                )}
              </Can>
            </Col>
          </Row>
          <br />
          <Row>
            <Col lg={45} md={45} sm={45}>
              <Can
                do={"api_mutations_update_finding_description_mutate"}
                passThrough={true}
              >
                {(canEdit: boolean): JSX.Element => (
                  <Editable
                    currentValue={dataset.threat}
                    isEditing={isEditing && canEdit}
                    label={t("searchFindings.tabDescription.threat.text")}
                    tooltip={t("searchFindings.tabDescription.threat.tooltip")}
                  >
                    <TextArea
                      id={"searchFindings.tabDescription.threat.tooltip"}
                      label={t("searchFindings.tabDescription.threat.text")}
                      name={"threat"}
                      tooltip={t(
                        "searchFindings.tabDescription.threat.tooltip"
                      )}
                      validate={composeValidators([
                        required,
                        validTextField,
                        maxThreatLength,
                      ])}
                    />
                  </Editable>
                )}
              </Can>
            </Col>
          </Row>
          <br />
          <Row>
            <Col>
              <Can
                do={"api_mutations_update_finding_description_mutate"}
                passThrough={true}
              >
                {(canEdit: boolean): JSX.Element => (
                  <Editable
                    currentValue={dataset.recommendation}
                    isEditing={isEditing && canEdit}
                    label={t(
                      "searchFindings.tabDescription.recommendation.text"
                    )}
                    tooltip={t(
                      "searchFindings.tabDescription.recommendation.tooltip"
                    )}
                  >
                    <TextArea
                      id={
                        "searchFindings.tabDescription.recommendation.tooltip"
                      }
                      label={t(
                        "searchFindings.tabDescription.recommendation.text"
                      )}
                      name={"recommendation"}
                      tooltip={t(
                        "searchFindings.tabDescription.recommendation.tooltip"
                      )}
                      validate={composeValidators([
                        required,
                        validTextField,
                        maxRecommendationLength,
                      ])}
                    />
                  </Editable>
                )}
              </Can>
            </Col>
          </Row>
          <br />
          <Can do={"api_mutations_update_finding_description_mutate"}>
            {isEditing ? (
              <Row>
                <Col lg={45} md={45} sm={45}>
                  <Tooltip
                    id={"searchFindings.tabDescription.sorts.tooltip"}
                    tip={t("searchFindings.tabDescription.sorts.tooltip")}
                  >
                    <FormGroup>
                      <Select
                        label={t("searchFindings.tabDescription.sorts.text")}
                        name={"sorts"}
                        validate={composeValidators([required])}
                      >
                        <option value={""} />
                        <option value={"NO"}>
                          {t("group.findings.boolean.False")}
                        </option>
                        <option value={"YES"}>
                          {t("group.findings.boolean.True")}
                        </option>
                      </Select>
                    </FormGroup>
                  </Tooltip>
                </Col>
              </Row>
            ) : undefined}
          </Can>
        </div>
      </div>
    </Form>
  );
};

export { DescriptionViewForm };
