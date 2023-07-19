import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useEffect, useMemo } from "react";
import { useTranslation } from "react-i18next";

import { Card } from "components/Card";
import { Col, Row } from "components/Layout";
import { Timeline } from "components/Timeline";
import { GET_VULN_TREATMENT } from "scenes/Dashboard/components/Vulnerabilities/TrackingTreatment/queries";
import type {
  IGetVulnTreatmentAttr,
  IHistoricTreatmentEdge,
} from "scenes/Dashboard/components/Vulnerabilities/TrackingTreatment/types";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/Finding-Content/DescriptionView/types";
import { formatDropdownField } from "utils/formatHelpers";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

interface ITreatmentTrackingAttr {
  vulnId: string;
}

export const TreatmentTracking: React.FC<ITreatmentTrackingAttr> = ({
  vulnId,
}: ITreatmentTrackingAttr): JSX.Element => {
  const { t } = useTranslation();

  const { data, fetchMore } = useQuery<IGetVulnTreatmentAttr>(
    GET_VULN_TREATMENT,
    {
      fetchPolicy: "network-only",
      nextFetchPolicy: "cache-first",
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning(
            "An error occurred loading the vulnerability historic treatment",
            error
          );
        });
      },
      variables: {
        vulnId,
      },
    }
  );
  const {
    pageInfo: treatmentPageInfo = {
      endCursor: "",
      hasNextPage: false,
    },
    edges: treatmentEdges = [],
  } = data === undefined ? {} : data.vulnerability.historicTreatmentConnection;

  const reversedHistoricTreatment = useMemo(
    (): IHistoricTreatment[] =>
      treatmentEdges
        .map((edge: IHistoricTreatmentEdge): IHistoricTreatment => edge.node)
        .reduce(
          (
            currentValue: IHistoricTreatment[],
            treatment: IHistoricTreatment,
            index: number,
            array: IHistoricTreatment[]
          ): IHistoricTreatment[] => {
            const isAcceptedUndefined: boolean =
              treatment.treatment === "ACCEPTED_UNDEFINED";

            if (
              (index === 0 ||
                (index < array.length - 1 &&
                  treatment.treatment !== array[index + 1].treatment)) &&
              !isAcceptedUndefined
            ) {
              return [...currentValue, treatment];
            }
            if (
              isAcceptedUndefined &&
              treatment.acceptanceStatus === "APPROVED"
            ) {
              return [
                ...currentValue,
                { ...treatment, acceptanceDate: array[index - 1].date },
              ];
            }
            if (
              isAcceptedUndefined &&
              treatment.acceptanceStatus === "REJECTED"
            ) {
              return [...currentValue, treatment];
            }

            if (
              !isAcceptedUndefined ||
              index === array.length - 1 ||
              treatment.treatment !== array[index + 1].treatment
            ) {
              return [...currentValue, treatment];
            }

            return currentValue;
          },
          []
        )
        .reduce(
          (
            previousValue: IHistoricTreatment[],
            current: IHistoricTreatment
          ): IHistoricTreatment[] => [current, ...previousValue],
          []
        ),
    [treatmentEdges]
  );

  useEffect((): void => {
    if (treatmentPageInfo.hasNextPage) {
      void fetchMore({
        variables: {
          after: treatmentPageInfo.endCursor,
        },
      });
    }
  }, [fetchMore, treatmentPageInfo]);

  return (
    <React.StrictMode>
      <Row justify={"center"}>
        <Col>
          <Timeline>
            {reversedHistoricTreatment.map((treatment): JSX.Element => {
              const pendingApproval =
                treatment.treatment === "ACCEPTED_UNDEFINED" &&
                treatment.acceptanceStatus !== "APPROVED";

              const approved =
                treatment.treatment === "ACCEPTED_UNDEFINED" &&
                treatment.acceptanceStatus === "APPROVED";

              const assignedUser = _.isEmpty(treatment.assigned)
                ? treatment.user
                : treatment.assigned;

              return (
                <Card float={true} key={treatment.date} title={treatment.date}>
                  <h3>
                    {t(formatDropdownField(treatment.treatment))}
                    {pendingApproval
                      ? t(
                          "searchFindings.tabDescription.treatment.pendingApproval"
                        )
                      : undefined}
                  </h3>
                  <p>
                    {assignedUser === undefined ||
                    treatment.treatment === "UNTREATED" ? undefined : (
                      <span>
                        {t("searchFindings.tabTracking.assigned")}
                        &nbsp;{assignedUser}
                        <br />
                      </span>
                    )}
                    {_.isEmpty(treatment.justification) ? undefined : (
                      <span>
                        {t("searchFindings.tabTracking.justification")}
                        &nbsp;{treatment.justification}
                        <br />
                      </span>
                    )}
                    {approved ? (
                      <span>
                        {t(
                          "searchFindings.tabVuln.contentTab.tracking.requestDate"
                        )}
                        &nbsp;{treatment.acceptanceDate}
                        <br />
                        {t(
                          "searchFindings.tabVuln.contentTab.tracking.requestApproval"
                        )}
                        &nbsp;{treatment.user}
                      </span>
                    ) : undefined}
                  </p>
                </Card>
              );
            })}
          </Timeline>
        </Col>
      </Row>
    </React.StrictMode>
  );
};
