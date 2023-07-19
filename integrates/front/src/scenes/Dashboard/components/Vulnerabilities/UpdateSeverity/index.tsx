import { useMutation, useQuery } from "@apollo/client";
import { faExternalLinkAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Formik } from "formik";
import type { GraphQLError } from "graphql";
import React, { Fragment, useCallback } from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import type { IUpdateSeverityProps } from "./types";

import { ExternalLink } from "components/ExternalLink";
import { Editable, Input, Label } from "components/Input";
import { ModalConfirm } from "components/Modal/Confirm";
import { Tooltip } from "components/Tooltip";
import {
  GET_VULN_SEVERITY_INFO,
  UPDATE_VULNERABILITIES_SEVERITY,
} from "scenes/Dashboard/components/Vulnerabilities/SeverityInfo/queries";
import type {
  IUpdateVulnsSeverityAttr,
  IVulnSeverityAttr,
} from "scenes/Dashboard/components/Vulnerabilities/SeverityInfo/types";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/Finding-Content/queries";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const BASE_URL = "https://www.first.org/cvss/calculator/3.1";
const CVSS_V3_DEFAULT = "CVSS:3.1/AV:P/AC:H/PR:H/UI:R/S:U/C:N/I:N/A:N";

export const UpdateSeverity: React.FC<IUpdateSeverityProps> = ({
  findingId,
  vulnerabilities,
  handleCloseModal,
  refetchData,
}: IUpdateSeverityProps): JSX.Element => {
  const { t } = useTranslation();

  const vulnerabilityIds = vulnerabilities.map(({ id }): string => id);

  const { data } = useQuery<IVulnSeverityAttr>(GET_VULN_SEVERITY_INFO, {
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading the severity info", error);
      });
    },
    variables: {
      vulnId: vulnerabilityIds[0],
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
          handleCloseModal();
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
      ],
    }
  );

  const onSubmit = useCallback(
    async (values: { severityVector: string }): Promise<void> => {
      await updateVulnerabilitiesSeverity({
        variables: {
          cvssVector: values.severityVector,
          findingId,
          vulnerabilityIds,
        },
      });
    },
    [findingId, vulnerabilityIds, updateVulnerabilitiesSeverity]
  );

  return (
    <React.StrictMode>
      <Formik
        enableReinitialize={true}
        initialValues={{
          severityVector: data?.vulnerability.severityVector ?? CVSS_V3_DEFAULT,
        }}
        name={"updateVulnerabilitiesSeverity"}
        onSubmit={onSubmit}
        validationSchema={object().shape({
          severityVector: string().required(t("validations.required")),
        })}
      >
        {({ isValid, submitForm, values }): React.ReactNode => {
          return (
            <Fragment>
              <Editable
                currentValue={
                  data?.vulnerability.severityVector ?? CVSS_V3_DEFAULT
                }
                isEditing={true}
                label={""}
              >
                <Label>
                  <b>
                    {t(
                      "searchFindings.tabDescription.updateVulnerabilitiesSeverityLabel"
                    )}
                  </b>
                  <ExternalLink href={`${BASE_URL}#${values.severityVector}`}>
                    <Tooltip
                      disp={"inline-block"}
                      id={"cvssCalculatorLink-tooltip"}
                      place={"bottom"}
                      tip={t(
                        "searchFindings.tabDescription.updateVulnerabilitiesSeverityTooltip"
                      )}
                    >
                      <FontAwesomeIcon icon={faExternalLinkAlt} />
                    </Tooltip>
                  </ExternalLink>
                </Label>
                <Input
                  name={"severityVector"}
                  placeholder={t(
                    "searchFindings.tabDescription.updateVulnerabilitiesSeverityPlaceholder"
                  )}
                />
              </Editable>
              <ModalConfirm
                disabled={!isValid}
                onCancel={handleCloseModal}
                onConfirm={submitForm}
                txtCancel={t("group.findings.report.modalClose")}
              />
            </Fragment>
          );
        }}
      </Formik>
    </React.StrictMode>
  );
};
