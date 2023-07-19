import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faExternalLinkAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Form, Formik } from "formik";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Card } from "components/Card";
import { Input } from "components/Input";
import { Col } from "components/Layout/Col";
import { Row } from "components/Layout/Row";
import { Text } from "components/Text";
import { Tooltip } from "components/Tooltip";
import { Can } from "context/authz/Can";
import { authzPermissionsContext } from "context/authz/config";
import { PoliciesLink } from "scenes/Dashboard/containers/Organization-Content/PoliciesView/styles";
import type { IPolicies } from "scenes/Dashboard/containers/Organization-Content/PoliciesView/types";
import { validateSchema } from "scenes/Dashboard/containers/Organization-Content/PoliciesView/validations";

const translationStart = "organization.tabs.policies.";
const policiesUrl =
  "https://docs.fluidattacks.com/tech/platform/organization/policies";

const Policies: React.FC<IPolicies> = ({
  handleSubmit,
  loadingPolicies,
  maxAcceptanceDays,
  maxAcceptanceSeverity,
  maxNumberAcceptances,
  minAcceptanceSeverity,
  minBreakingSeverity,
  permission,
  vulnerabilityGracePeriod,
  savingPolicies,
  tooltipMessage = undefined,
  inactivityPeriod = undefined,
}: IPolicies): JSX.Element => {
  const { t } = useTranslation();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);

  return (
    <Formik
      enableReinitialize={true}
      initialValues={{
        inactivityPeriod: _.isNil(inactivityPeriod)
          ? ""
          : inactivityPeriod.toString(),
        maxAcceptanceDays: _.isNull(maxAcceptanceDays)
          ? ""
          : maxAcceptanceDays.toString(),
        maxAcceptanceSeverity: parseFloat(maxAcceptanceSeverity)
          .toFixed(1)
          .toString(),
        maxNumberAcceptances: _.isNull(maxNumberAcceptances)
          ? ""
          : maxNumberAcceptances.toString(),
        minAcceptanceSeverity: parseFloat(minAcceptanceSeverity)
          .toFixed(1)
          .toString(),
        minBreakingSeverity: _.isNull(minBreakingSeverity)
          ? ""
          : parseFloat(minBreakingSeverity).toFixed(1).toString(),
        vulnerabilityGracePeriod: _.isNull(vulnerabilityGracePeriod)
          ? ""
          : vulnerabilityGracePeriod.toString(),
      }}
      name={"policies"}
      onSubmit={handleSubmit}
      validationSchema={validateSchema(_.isNil(inactivityPeriod))}
    >
      {({ dirty, isSubmitting }): JSX.Element => (
        <Form id={"policies"}>
          {tooltipMessage === undefined ? (
            <Text fw={7} mb={3} mt={4} size={"big"}>
              {t(`${translationStart}title`)}
            </Text>
          ) : (
            <Tooltip
              disp={"inline-block"}
              id={"policies.tooltip.id"}
              tip={tooltipMessage}
            >
              <Text fw={7} mb={3} mt={4} size={"big"}>
                {t(`${translationStart}title`)}
              </Text>
            </Tooltip>
          )}
          <Row>
            <Col lg={33} md={50} sm={100}>
              <Card>
                <label className={"db mb1"} htmlFor={"maxAcceptanceDays"}>
                  <Text disp={"inline"} fw={4} mr={1}>
                    {t(`${translationStart}policies.maxAcceptanceDays`)}
                  </Text>
                  <PoliciesLink
                    href={`${policiesUrl}#maximum-number-of-calendar-days-a-finding-can-be-temporarily-accepted`}
                  >
                    <Tooltip
                      disp={"inline-block"}
                      id={"maxAcceptanceDays-tooltip"}
                      place={"bottom"}
                      tip={t(`${translationStart}externalTooltip`)}
                    >
                      <FontAwesomeIcon icon={faExternalLinkAlt} />
                    </Tooltip>
                  </PoliciesLink>
                </label>
                <Input
                  disabled={permissions.cannot(permission)}
                  name={"maxAcceptanceDays"}
                  tooltip={t(
                    `${translationStart}recommended.maxAcceptanceDays`
                  )}
                  type={"text"}
                />
              </Card>
            </Col>
            <Col lg={33} md={50} sm={100}>
              <Card>
                <label className={"db mb1"} htmlFor={"maxNumberAcceptances"}>
                  <Text disp={"inline"} fw={4} mr={1}>
                    {t(`${translationStart}policies.maxNumberAcceptances`)}
                  </Text>
                  <PoliciesLink
                    href={`${policiesUrl}#maximum-number-of-times-a-finding-can-be-accepted`}
                  >
                    <Tooltip
                      disp={"inline-block"}
                      id={"maxNumberAcceptances-tooltip"}
                      place={"bottom"}
                      tip={t(`${translationStart}externalTooltip`)}
                    >
                      <FontAwesomeIcon icon={faExternalLinkAlt} />
                    </Tooltip>
                  </PoliciesLink>
                </label>
                <Input
                  disabled={permissions.cannot(permission)}
                  name={"maxNumberAcceptances"}
                  tooltip={t(
                    `${translationStart}recommended.maxNumberAcceptances`
                  )}
                  type={"text"}
                />
              </Card>
            </Col>
            <Col lg={33} md={50} sm={100}>
              <Card>
                <label
                  className={"db mb1"}
                  htmlFor={"vulnerabilityGracePeriod"}
                >
                  <Text disp={"inline"} fw={4} mr={1}>
                    {t(`${translationStart}policies.vulnerabilityGracePeriod`)}
                  </Text>
                  <PoliciesLink
                    href={`${policiesUrl}#grace-period-where-newly-reported-vulnerabilities-wont-break-the-build`}
                  >
                    <Tooltip
                      disp={"inline-block"}
                      id={"vulnerabilityGracePeriod-tooltip"}
                      place={"bottom"}
                      tip={t(`${translationStart}externalTooltip`)}
                    >
                      <FontAwesomeIcon icon={faExternalLinkAlt} />
                    </Tooltip>
                  </PoliciesLink>
                </label>
                <Input
                  disabled={permissions.cannot(permission)}
                  name={"vulnerabilityGracePeriod"}
                  tooltip={t(
                    `${translationStart}recommended.vulnerabilityGracePeriod`
                  )}
                  type={"text"}
                />
              </Card>
            </Col>
          </Row>
          <Row>
            <Col lg={33} md={50} sm={100}>
              <Card>
                <label className={"db mb1"} htmlFor={"minAcceptanceSeverity"}>
                  <Text disp={"inline"} fw={4} mr={1}>
                    {t(`${translationStart}policies.minAcceptanceSeverity`)}
                  </Text>
                  <PoliciesLink
                    href={`${policiesUrl}#temporal-acceptance-minimum-cvss-31-score-allowed-for-assignment`}
                  >
                    <Tooltip
                      disp={"inline-block"}
                      id={"minAcceptanceSeverity-tooltip"}
                      place={"bottom"}
                      tip={t(`${translationStart}externalTooltip`)}
                    >
                      <FontAwesomeIcon icon={faExternalLinkAlt} />
                    </Tooltip>
                  </PoliciesLink>
                </label>
                <Input
                  disabled={permissions.cannot(permission)}
                  name={"minAcceptanceSeverity"}
                  tooltip={t(
                    `${translationStart}recommended.minAcceptanceSeverity`
                  )}
                  type={"text"}
                />
              </Card>
            </Col>
            <Col lg={33} md={50} sm={100}>
              <Card>
                <label className={"db mb1"} htmlFor={"maxAcceptanceSeverity"}>
                  <Text disp={"inline"} fw={4} mr={1}>
                    {t(`${translationStart}policies.maxAcceptanceSeverity`)}
                  </Text>
                  <PoliciesLink
                    href={`${policiesUrl}#temporal-acceptance-maximum-cvss-31-score-allowed-for-assignment`}
                  >
                    <Tooltip
                      disp={"inline-block"}
                      id={"maxAcceptanceSeverity-tooltip"}
                      place={"bottom"}
                      tip={t(`${translationStart}externalTooltip`)}
                    >
                      <FontAwesomeIcon icon={faExternalLinkAlt} />
                    </Tooltip>
                  </PoliciesLink>
                </label>
                <Input
                  disabled={permissions.cannot(permission)}
                  name={"maxAcceptanceSeverity"}
                  tooltip={t(
                    `${translationStart}recommended.maxAcceptanceSeverity`
                  )}
                  type={"text"}
                />
              </Card>
            </Col>
            <Col lg={33} md={50} sm={100}>
              <Card>
                <label className={"db mb1"} htmlFor={"minBreakingSeverity"}>
                  <Text disp={"inline"} fw={4} mr={1}>
                    {t(`${translationStart}policies.minBreakingSeverity`)}
                  </Text>
                  <PoliciesLink
                    href={`${policiesUrl}#minimum-cvss-31-score-of-an-open-vulnerability-for-devsecops`}
                  >
                    <Tooltip
                      disp={"inline-block"}
                      id={"minBreakingSeverity-tooltip"}
                      place={"bottom"}
                      tip={t(`${translationStart}externalTooltip`)}
                    >
                      <FontAwesomeIcon icon={faExternalLinkAlt} />
                    </Tooltip>
                  </PoliciesLink>
                </label>
                <Input
                  disabled={permissions.cannot(permission)}
                  name={"minBreakingSeverity"}
                  tooltip={t(
                    `${translationStart}recommended.minBreakingSeverity`
                  )}
                  type={"text"}
                />
              </Card>
            </Col>
          </Row>
          {_.isNil(inactivityPeriod) ? undefined : (
            <Row>
              <Col lg={33} md={50} sm={100}>
                <Card>
                  <label className={"db mb1"} htmlFor={"inactivityPeriod"}>
                    <Text disp={"inline"} fw={4} mr={1}>
                      {t(`${translationStart}policies.inactivityPeriod`)}
                    </Text>
                    <PoliciesLink
                      href={`${policiesUrl}#login-inactivity-number-of-days-for-stakeholders-inactivity-period`}
                    >
                      <Tooltip
                        disp={"inline-block"}
                        id={"inactivityPeriod-tooltip"}
                        place={"bottom"}
                        tip={t(`${translationStart}externalTooltip`)}
                      >
                        <FontAwesomeIcon icon={faExternalLinkAlt} />
                      </Tooltip>
                    </PoliciesLink>
                  </label>
                  <Input
                    disabled={permissions.cannot(permission)}
                    name={"inactivityPeriod"}
                    tooltip={t(
                      `${translationStart}recommended.inactivityPeriod`
                    )}
                    type={"text"}
                  />
                </Card>
              </Col>
            </Row>
          )}
          <div className={"mt2"} />
          <Can do={permission}>
            {!dirty ||
            loadingPolicies ||
            isSubmitting ||
            savingPolicies ? undefined : (
              <Button type={"submit"} variant={"secondary"}>
                {t(`${translationStart}save`)}
              </Button>
            )}
          </Can>
        </Form>
      )}
    </Formik>
  );
};

export { Policies };
