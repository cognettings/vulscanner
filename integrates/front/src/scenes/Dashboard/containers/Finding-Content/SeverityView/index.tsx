import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faPen, faRotateRight } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { Button } from "components/Button/index";
import { Editable, Label, Select } from "components/Input";
import { FormGroup } from "components/Input/styles";
import { ButtonToolbarRow, Col, Row } from "components/Layout";
import { Tooltip } from "components/Tooltip";
import { Can } from "context/authz/Can";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/Finding-Content/queries";
import {
  GET_SEVERITY,
  UPDATE_SEVERITY_MUTATION,
} from "scenes/Dashboard/containers/Finding-Content/SeverityView/queries";
import { SeverityContent } from "scenes/Dashboard/containers/Finding-Content/SeverityView/SeverityContent/index";
import type {
  ISeverityAttr,
  ISeverityField,
  IUpdateSeverityAttr,
} from "scenes/Dashboard/containers/Finding-Content/SeverityView/types";
import { castFieldsCVSS3 } from "scenes/Dashboard/containers/Finding-Content/SeverityView/utils";
import { getCVSS31Values, getCVSS31VectorString } from "utils/cvss";
import type { ICVSS3EnvironmentalMetrics } from "utils/cvss";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { required } from "utils/validations";

const SeverityView: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { findingId } = useParams<{ findingId: string }>();
  const [isEditing, setIsEditing] = useState(false);
  const CVSS_VERSION = "3.1";

  const handleErrors: (error: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred loading finding severity", error);
    });
  };

  const { data, refetch } = useQuery<ISeverityAttr>(GET_SEVERITY, {
    onError: handleErrors,
    variables: { identifier: findingId },
  });

  const handleEditClick = useCallback((): void => {
    setIsEditing(!isEditing);
  }, [isEditing]);

  const handleMtUpdateSeverityRes: (mtResult: IUpdateSeverityAttr) => void = (
    mtResult: IUpdateSeverityAttr
  ): void => {
    if (!_.isUndefined(mtResult)) {
      if (mtResult.updateSeverity.success) {
        void refetch();
        msgSuccess(t("groupAlerts.updated"), t("groupAlerts.updatedTitle"));
        mixpanel.track("UpdateSeverity");
      }
    }
  };

  const handleMtError = (errors: ApolloError): void => {
    errors.graphQLErrors.forEach((error: GraphQLError): void => {
      switch (error.message) {
        case "Exception - Severity score is invalid":
          msgError(t("validations.addFindingModal.invalidSeverityScore"));
          break;
        case "Exception - Invalid characters":
          msgError(t("validations.invalidChar"));
          break;
        default:
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred updating severity", error);
      }
    });
  };

  const [updateSeverity, mutationRes] = useMutation(UPDATE_SEVERITY_MUTATION, {
    onCompleted: handleMtUpdateSeverityRes,
    onError: handleMtError,
    refetchQueries: [
      {
        query: GET_FINDING_HEADER,
        variables: {
          findingId,
        },
      },
    ],
  });

  const handleUpdateSeverity: (values: ICVSS3EnvironmentalMetrics) => void =
    useCallback(
      (values: ICVSS3EnvironmentalMetrics): void => {
        setIsEditing(false);
        void updateSeverity({
          variables: {
            attackComplexity: "0.0",
            attackVector: "0.0",
            availabilityImpact: "0.0",
            availabilityRequirement: "0.0",
            confidentialityImpact: "0.0",
            confidentialityRequirement: "0.0",
            cvssVector: getCVSS31VectorString(values),
            cvssVersion: CVSS_VERSION,
            exploitability: "0.0",
            findingId,
            integrityImpact: "0.0",
            integrityRequirement: "0.0",
            modifiedAttackComplexity: "0.0",
            modifiedAttackVector: "0.0",
            modifiedAvailabilityImpact: "0.0",
            modifiedConfidentialityImpact: "0.0",
            modifiedIntegrityImpact: "0.0",
            modifiedPrivilegesRequired: "0.0",
            modifiedSeverityScope: "0.0",
            modifiedUserInteraction: "0.0",
            privilegesRequired: "0.0",
            remediationLevel: "0.0",
            reportConfidence: "0.0",
            severityScope: "0.0",
            userInteraction: "0.0",
          },
        });
      },
      [findingId, updateSeverity]
    );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const cvss31Values = getCVSS31Values(data.finding.severityVector);

  return (
    <React.StrictMode>
      <Row>
        <Col>
          <React.Fragment>
            <Can do={"api_mutations_update_severity_mutate"}>
              <ButtonToolbarRow>
                <Tooltip
                  id={"severityEditTooltip"}
                  tip={t("searchFindings.tabSeverity.editable.tooltip")}
                >
                  <Button onClick={handleEditClick} variant={"secondary"}>
                    <FontAwesomeIcon icon={faPen} />
                    &nbsp;
                    {t("searchFindings.tabSeverity.editable.label")}
                  </Button>
                </Tooltip>
              </ButtonToolbarRow>
            </Can>
            <br />
            {isEditing ? (
              <Formik
                enableReinitialize={true}
                initialValues={cvss31Values}
                name={"editSeverity"}
                onSubmit={handleUpdateSeverity}
              >
                {({ dirty }): React.ReactNode => (
                  <Form id={"editSeverity"}>
                    <React.Fragment>
                      <ButtonToolbarRow>
                        <Button
                          disabled={!dirty || mutationRes.loading}
                          type={"submit"}
                          variant={"primary"}
                        >
                          <FontAwesomeIcon icon={faRotateRight} />
                          {t("searchFindings.tabSeverity.update")}
                        </Button>
                      </ButtonToolbarRow>
                      <div className={"w-25"}>
                        <Row>
                          <FormGroup>
                            <Label>
                              <b>
                                {`${t(
                                  "searchFindings.tabSeverity.cvssVersion"
                                )}: ${CVSS_VERSION}`}
                              </b>
                            </Label>
                          </FormGroup>
                        </Row>
                      </div>
                    </React.Fragment>
                    {castFieldsCVSS3(cvss31Values).map(
                      (field: ISeverityField, index: number): JSX.Element => {
                        const currentOption: string =
                          field.options[field.currentValue];

                        return (
                          <div className={"w-25"} key={field.name}>
                            <Row>
                              <Editable
                                currentValue={`${field.currentValue} | ${t(
                                  currentOption
                                )}`}
                                isEditing={true}
                                label={field.title}
                              >
                                <Select
                                  id={`Row${index}`}
                                  label={field.title}
                                  name={field.name}
                                  validate={required}
                                >
                                  <option value={""} />
                                  {_.map(
                                    field.options,
                                    (
                                      text: string,
                                      value: string
                                    ): JSX.Element => (
                                      <option key={text} value={value}>
                                        {t(text)}
                                      </option>
                                    )
                                  )}
                                </Select>
                              </Editable>
                            </Row>
                          </div>
                        );
                      }
                    )}
                  </Form>
                )}
              </Formik>
            ) : (
              <SeverityContent
                /* eslint-disable-next-line react/jsx-props-no-spreading -- Preferred for readability */
                {...cvss31Values}
              />
            )}
          </React.Fragment>
        </Col>
      </Row>
    </React.StrictMode>
  );
};

export { SeverityView };
