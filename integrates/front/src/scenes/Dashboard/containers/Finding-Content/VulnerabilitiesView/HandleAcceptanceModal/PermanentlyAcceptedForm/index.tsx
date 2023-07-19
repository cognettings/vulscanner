import type { ApolloError } from "@apollo/client";
import { useMutation } from "@apollo/client";
import { Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { AcceptedUndefinedTable } from "./AcceptedUndefinedTable";
import type { IFormValues, IPermanentlyAcceptedFormProps } from "./types";
import { getAllNotifications } from "./utils";

import { getVulnsPendingOfAcceptance } from "../../utils";
import { isAcceptedUndefinedSelectedHelper } from "../helpers";
import { HANDLE_VULNS_ACCEPTANCE } from "../queries";
import type {
  IHandleVulnerabilitiesAcceptanceResultAttr,
  IVulnDataAttr,
  VulnUpdateResult,
} from "../types";
import { TextArea } from "components/Input";
import { ModalConfirm } from "components/Modal";
import { GET_ME_VULNERABILITIES_ASSIGNED_IDS } from "pages/home/dashboard/navbar/to-do/queries";
import { getAreAllNotificationValid } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/helpers";
import { SEND_ASSIGNED_NOTIFICATION } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/queries";
import type { ISendNotificationResultAttr } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/types";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const PermanentlyAcceptedForm: React.FC<IPermanentlyAcceptedFormProps> = ({
  onCancel,
  refetchData,
  vulnerabilities,
}: IPermanentlyAcceptedFormProps): JSX.Element => {
  const { t } = useTranslation();

  // State
  const [acceptanceVulnerabilities, setAcceptanceVulnerabilities] = useState<
    IVulnDataAttr[]
  >(getVulnsPendingOfAcceptance(vulnerabilities));
  const [acceptedVulnerabilities, setAcceptedVulnerabilities] = useState<
    IVulnDataAttr[]
  >([]);
  const [rejectedVulnerabilities, setRejectedVulnerabilities] = useState<
    IVulnDataAttr[]
  >([]);

  // GraphQL operations
  const [handleAcceptance, { loading, client }] =
    useMutation<IHandleVulnerabilitiesAcceptanceResultAttr>(
      HANDLE_VULNS_ACCEPTANCE
    );

  const [sendNotification] = useMutation<ISendNotificationResultAttr>(
    SEND_ASSIGNED_NOTIFICATION,
    {
      onError: (updateError: ApolloError): void => {
        updateError.graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(
            t(
              "searchFindings.tabDescription.notification.emailNotificationError"
            )
          );
          Logger.warning("An error occurred sending the notification", error);
        });
      },
    }
  );

  const handleNotification = useCallback(async (): Promise<void> => {
    if (acceptedVulnerabilities.length > 0) {
      const notificationsResults = await getAllNotifications(
        sendNotification,
        acceptedVulnerabilities
      );
      const areAllNotificationValid =
        getAreAllNotificationValid(notificationsResults);
      if (areAllNotificationValid.every(Boolean)) {
        msgSuccess(
          t(
            "searchFindings.tabDescription.notification.altEmailNotificationText"
          ),
          t("searchFindings.tabDescription.notification.emailNotificationTitle")
        );
      }
    }
  }, [acceptedVulnerabilities, sendNotification, t]);

  // Handle actions
  const handleSubmit = useCallback(
    async (formValues: IFormValues): Promise<void> => {
      try {
        await isAcceptedUndefinedSelectedHelper(
          handleAcceptance,
          acceptedVulnerabilities,
          formValues,
          rejectedVulnerabilities
        ).then(async (allValues: VulnUpdateResult[][]): Promise<void> => {
          const areAllValid = allValues
            .map((values: VulnUpdateResult[]): boolean[] => {
              return values.map((result: VulnUpdateResult): boolean => {
                if (!_.isUndefined(result.data) && !_.isNull(result.data)) {
                  return _.isUndefined(
                    result.data.handleVulnerabilitiesAcceptance
                  )
                    ? true
                    : result.data.handleVulnerabilitiesAcceptance.success;
                }

                return false;
              });
            })
            .reduce(
              (previous: boolean[], current: boolean[]): boolean[] => [
                ...previous,
                ...current,
              ],
              []
            );
          if (areAllValid.every(Boolean)) {
            msgSuccess(
              t("searchFindings.tabVuln.alerts.acceptanceSuccess"),
              t("groupAlerts.updatedTitle")
            );
          }
          onCancel();
          refetchData();
          await handleNotification();
        });
      } catch (requestError: unknown) {
        switch (String(requestError).replace(/^Error: /u, "")) {
          case "Exception - It cant handle acceptance without being requested":
            msgError(t("searchFindings.tabVuln.alerts.acceptanceNotRequested"));
            break;
          case "Exception - Vulnerability not found":
            msgError(t("groupAlerts.noFound"));
            break;
          case "Exception - Invalid characters":
            msgError(t("validations.invalidChar"));
            break;
          default:
            msgError(t("groupAlerts.errorTextsad"));
            Logger.warning(
              "An error occurred handling acceptance",
              requestError
            );
        }
      } finally {
        await client.refetchQueries({
          include: [GET_ME_VULNERABILITIES_ASSIGNED_IDS],
        });
      }
    },
    [
      acceptedVulnerabilities,
      client,
      handleAcceptance,
      handleNotification,
      onCancel,
      refetchData,
      rejectedVulnerabilities,
      t,
    ]
  );

  // Side effects
  useEffect((): void => {
    setAcceptedVulnerabilities(
      acceptanceVulnerabilities.reduce(
        (acc: IVulnDataAttr[], vulnerability: IVulnDataAttr): IVulnDataAttr[] =>
          vulnerability.acceptance === "APPROVED"
            ? [...acc, vulnerability]
            : acc,
        []
      )
    );
    setRejectedVulnerabilities(
      acceptanceVulnerabilities.reduce(
        (acc: IVulnDataAttr[], vulnerability: IVulnDataAttr): IVulnDataAttr[] =>
          vulnerability.acceptance === "REJECTED"
            ? [...acc, vulnerability]
            : acc,
        []
      )
    );
  }, [acceptanceVulnerabilities]);

  return (
    <Formik
      enableReinitialize={true}
      initialValues={{ justification: "" }}
      name={"permanentlyAcceptedForm"}
      onSubmit={handleSubmit}
      validationSchema={object().shape({
        justification: string().required(t("validations.required")),
      })}
    >
      <Form id={"permanentlyAcceptedForm"}>
        <AcceptedUndefinedTable
          acceptanceVulns={acceptanceVulnerabilities}
          isAcceptedUndefinedSelected={true}
          setAcceptanceVulns={setAcceptanceVulnerabilities}
        />
        <br />
        <TextArea
          label={t(
            "searchFindings.tabDescription.remediationModal.observations"
          )}
          name={"justification"}
          required={true}
        />
        <br />
        <ModalConfirm
          disabled={
            (acceptedVulnerabilities.length === 0 &&
              rejectedVulnerabilities.length === 0) ||
            loading
          }
          onCancel={onCancel}
        />
      </Form>
    </Formik>
  );
};

export { PermanentlyAcceptedForm };
