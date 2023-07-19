import { useMutation, useQuery } from "@apollo/client";
import { Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { Fragment, useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import {
  GET_VULN_SEVERITY_INFO,
  UPDATE_VULNERABILITIES_SEVERITY,
} from "./queries";
import type { IUpdateVulnsSeverityAttr, IVulnSeverityAttr } from "./types";

import { ActionButtons } from "../AdditionalInfo/ActionButtons";
import { Detail } from "../AdditionalInfo/detail";
import { ExternalLink } from "components/ExternalLink";
import { Input } from "components/Input/Fields/Input";
import { Row } from "components/Layout";
import { Can } from "context/authz/Can";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/Finding-Content/queries";
import { SeverityContent } from "scenes/Dashboard/containers/Finding-Content/SeverityView/SeverityContent/index";
import { getCVSS31Values } from "utils/cvss";
import { severityFormatter } from "utils/formatHelpers";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface ISeverityInfoProps {
  findingId: string;
  refetchData: () => void;
  vulnerabilityId: string;
}

const BASE_URL = "https://www.first.org/cvss/calculator/3.1";

export const SeverityInfo: React.FC<ISeverityInfoProps> = ({
  findingId,
  refetchData,
  vulnerabilityId,
}: ISeverityInfoProps): JSX.Element => {
  const { t } = useTranslation();
  const [isEditing, setIsEditing] = useState(false);

  const { data } = useQuery<IVulnSeverityAttr>(GET_VULN_SEVERITY_INFO, {
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading the severity info", error);
      });
    },
    variables: {
      vulnId: vulnerabilityId,
    },
  });

  const [updateVulnerabilitiesSeverity] = useMutation(
    UPDATE_VULNERABILITIES_SEVERITY,
    {
      onCompleted: (result: IUpdateVulnsSeverityAttr): void => {
        if (result.updateVulnerabilitiesSeverity.success) {
          msgSuccess(
            t("searchFindings.tabVuln.severityInfo.alerts.updatedSeverity"),
            t("groupAlerts.updatedTitle")
          );
          setIsEditing(false);
          refetchData();
        }
      },
      onError: ({ graphQLErrors }): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            case "Exception - Error invalid severity CVSS v3.1 vector string":
              msgError(
                t(
                  "searchFindings.tabVuln.severityInfo.alerts.invalidSeverityVector"
                )
              );
              break;
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning("An error occurred updating severity", error);
          }
        });
      },
      refetchQueries: [
        {
          query: GET_FINDING_HEADER,
          variables: {
            findingId,
          },
        },
        {
          query: GET_VULN_SEVERITY_INFO,
          variables: {
            vulnId: vulnerabilityId,
          },
        },
      ],
    }
  );

  const toggleEdit = useCallback((): void => {
    setIsEditing((currentValue: boolean): boolean => !currentValue);
  }, []);

  const onSubmit = useCallback(
    async (values: { severityVector: string }): Promise<void> => {
      await updateVulnerabilitiesSeverity({
        variables: {
          cvssVector: values.severityVector,
          findingId,
          vulnerabilityIds: [vulnerabilityId],
        },
      });
    },
    [findingId, vulnerabilityId, updateVulnerabilitiesSeverity]
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const cvss31Values = getCVSS31Values(data.vulnerability.severityVector);

  return (
    <React.StrictMode>
      <Row>
        <Formik
          enableReinitialize={true}
          initialValues={{
            severityVector: data.vulnerability.severityVector,
          }}
          name={"editVulnerabilitySeverity"}
          onSubmit={onSubmit}
          validationSchema={object().shape({
            severityVector: string().required(t("validations.required")),
          })}
        >
          {({ dirty, submitForm }): React.ReactNode => {
            return (
              <Fragment>
                <Can
                  do={"api_mutations_update_vulnerabilities_severity_mutate"}
                >
                  <ActionButtons
                    isEditing={isEditing}
                    isPristine={!dirty}
                    onEdit={toggleEdit}
                    onUpdate={submitForm}
                  />
                </Can>
                <Row>
                  <Detail
                    editableField={<Input name={"severityVector"} />}
                    field={
                      <ExternalLink
                        href={`${BASE_URL}#${data.vulnerability.severityVector}`}
                      >
                        {data.vulnerability.severityVector}
                      </ExternalLink>
                    }
                    isEditing={isEditing}
                    label={
                      <b>
                        {t(
                          "searchFindings.tabVuln.severityInfo.severityVectorTitle"
                        )}
                      </b>
                    }
                  />
                </Row>
              </Fragment>
            );
          }}
        </Formik>
      </Row>
      <br />
      {isEditing ? undefined : (
        <Row>
          <Row>
            <Detail
              editableField={undefined}
              field={severityFormatter(
                data.vulnerability.severityTemporalScore
              )}
              isEditing={false}
              label={
                <b>
                  {t(
                    "searchFindings.tabVuln.severityInfo.severityTemporalScore"
                  )}
                </b>
              }
            />
          </Row>
          <SeverityContent
            /* eslint-disable-next-line react/jsx-props-no-spreading -- Preferred for readability */
            {...cvss31Values}
          />
        </Row>
      )}
    </React.StrictMode>
  );
};
