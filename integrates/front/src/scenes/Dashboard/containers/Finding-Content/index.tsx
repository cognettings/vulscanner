import type { ApolloError } from "@apollo/client";
import { useMutation, useQuery } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useContext, useState } from "react";
import { useTranslation } from "react-i18next";
import {
  Redirect,
  Route,
  Switch,
  useHistory,
  useParams,
  useRouteMatch,
} from "react-router-dom";
import { mixed, object } from "yup";

import { FindingOverview } from "./overview";
import { ButtonCol, Title, TitleContainer } from "./styles";

import type { IGroupFindingsAttr } from "../Group-Content/GroupFindingsView/types";
import { Button } from "components/Button";
import { Select } from "components/Input";
import { FormGroup } from "components/Input/styles";
import { Modal, ModalConfirm } from "components/Modal";
import { Tab, TabContent, Tabs } from "components/Tabs";
import { Tooltip } from "components/Tooltip";
import { Can } from "context/authz/Can";
import { authzPermissionsContext } from "context/authz/config";
import { Have } from "context/authz/Have";
import { featurePreviewContext } from "context/featurePreview";
import { useTabTracking } from "hooks";
import { EventBar } from "scenes/Dashboard/components/EventBar";
import { CommentsView } from "scenes/Dashboard/containers/Finding-Content/CommentsView/index";
import { DescriptionView } from "scenes/Dashboard/containers/Finding-Content/DescriptionView/index";
import { EvidenceView } from "scenes/Dashboard/containers/Finding-Content/EvidenceView/index";
import { MachineView } from "scenes/Dashboard/containers/Finding-Content/MachineView/index";
import {
  GET_FINDING_HEADER,
  REMOVE_FINDING_MUTATION,
} from "scenes/Dashboard/containers/Finding-Content/queries";
import { RecordsView } from "scenes/Dashboard/containers/Finding-Content/RecordsView/index";
import { SeverityView } from "scenes/Dashboard/containers/Finding-Content/SeverityView/index";
import { TrackingView } from "scenes/Dashboard/containers/Finding-Content/TrackingView/index";
import type { IHeaderQueryResult } from "scenes/Dashboard/containers/Finding-Content/types";
import { VulnsView } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/index";
import { GET_FINDINGS } from "scenes/Dashboard/containers/Group-Content/GroupFindingsView/queries";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const FindingContent: React.FC = (): JSX.Element => {
  const { findingId, groupName, organizationName } = useParams<{
    findingId: string;
    groupName: string;
    organizationName: string;
  }>();
  const { featurePreview } = useContext(featurePreviewContext);
  const { t } = useTranslation();
  const { path, url } = useRouteMatch<{ path: string; url: string }>();
  const { replace } = useHistory();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canGetRejectedVulnerabilities: boolean = permissions.can(
    "api_resolvers_finding_rejected_vulnerabilities_resolve"
  );
  const canGetSubmittedVulnerabilities: boolean = permissions.can(
    "api_resolvers_finding_submitted_vulnerabilities_resolve"
  );

  // Side effects
  useTabTracking("Finding");

  // State management
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const openDeleteModal: () => void = useCallback((): void => {
    setIsDeleteModalOpen(true);
  }, []);
  const closeDeleteModal: () => void = useCallback((): void => {
    setIsDeleteModalOpen(false);
  }, []);

  // GraphQL operations
  const { data: headerData, refetch: refetchFindingHeader } =
    useQuery<IHeaderQueryResult>(GET_FINDING_HEADER, {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred loading finding header", error);
        });
      },
      variables: {
        canRetrieveHacker: permissions.can(
          "api_resolvers_finding_hacker_resolve"
        ),
        findingId,
      },
    });

  const [removeFinding, { loading: deleting }] = useMutation(
    REMOVE_FINDING_MUTATION,
    {
      onCompleted: (result: { removeFinding: { success: boolean } }): void => {
        if (result.removeFinding.success) {
          msgSuccess(
            t("searchFindings.findingDeleted", { findingId }),
            t("searchFindings.successTitle")
          );
          replace(`/orgs/${organizationName}/groups/${groupName}/vulns`);
        }
      },
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred deleting finding", error);
        });
      },
      refetchQueries: [GET_FINDINGS],
    }
  );

  const handleDelete = useCallback(
    async (values: Record<string, unknown>): Promise<void> => {
      await removeFinding({
        variables: { findingId, justification: values.justification },
      });
    },
    [removeFinding, findingId]
  );

  const handleQryErrors: (error: ApolloError) => void = useCallback(
    ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading group data", error);
      });
    },
    [t]
  );

  const { data } = useQuery<IGroupFindingsAttr>(GET_FINDINGS, {
    fetchPolicy: "cache-first",
    onError: handleQryErrors,
    variables: {
      canGetRejectedVulnerabilities,
      canGetSubmittedVulnerabilities,
      groupName,
    },
  });

  const groupOpenCVSSF =
    data?.group.findings
      .filter((find): boolean => find.status === "VULNERABLE")
      .reduce((sum, finding): number => sum + finding.totalOpenCVSSF, 0) ?? 0;

  if (_.isUndefined(headerData) || _.isEmpty(headerData)) {
    return <div />;
  }

  const isDraft: boolean = _.isEmpty(headerData.finding.releaseDate);

  const calculateEstRemediationTime = (): string => {
    if (_.isNil(headerData.finding.minTimeToRemediate)) {
      return "Unknown";
    }
    const minutesInAnHour = 60;
    const rawHours =
      (headerData.finding.minTimeToRemediate * headerData.finding.openVulns) /
      minutesInAnHour;

    if (rawHours === 0) {
      return "None";
    } else if (Number.isInteger(rawHours)) {
      return `${rawHours.toFixed(0)}h`;
    }

    return `${rawHours.toFixed(1)}h`;
  };

  const validations = object().shape({
    justification: mixed().required(t("validations.required")),
  });

  return (
    <React.StrictMode>
      <div>
        <div>
          <div>
            <div>
              <EventBar organizationName={organizationName} />
              <TitleContainer>
                <Title data-private={true}>{headerData.finding.title}</Title>
                <ButtonCol>
                  <Have I={"can_report_vulnerabilities"}>
                    <Can do={"api_mutations_remove_finding_mutate"}>
                      <Tooltip
                        disp={"inline-block"}
                        id={"searchFindings.delete.btn.tooltip"}
                        tip={t("searchFindings.delete.btn.tooltip")}
                      >
                        <Button onClick={openDeleteModal} variant={"secondary"}>
                          <FontAwesomeIcon icon={faTrashAlt} />
                          &nbsp;{t("searchFindings.delete.btn.text")}
                        </Button>
                      </Tooltip>
                    </Can>
                  </Have>
                </ButtonCol>
              </TitleContainer>
              <div>
                <FindingOverview
                  discoveryDate={
                    headerData.finding.releaseDate?.split(" ")[0] ?? "-"
                  }
                  estRemediationTime={calculateEstRemediationTime()}
                  findingOpenCVSSF={headerData.finding.totalOpenCVSSF}
                  groupOpenCVSSF={groupOpenCVSSF}
                  maxOpenSeverityScore={headerData.finding.maxOpenSeverityScore}
                  openVulns={headerData.finding.openVulns}
                  status={headerData.finding.status}
                />
                <br />
                <Tabs>
                  {featurePreview ? undefined : (
                    <Tab
                      id={"vulnItem"}
                      link={`${url}/locations`}
                      tooltip={t("searchFindings.tabVuln.tooltip")}
                    >
                      {t("searchFindings.tabVuln.tabTitle")}
                    </Tab>
                  )}
                  <Tab
                    id={"infoItem"}
                    link={`${url}/description`}
                    tooltip={t("searchFindings.tabDescription.tooltip")}
                  >
                    {t("searchFindings.tabDescription.tabTitle")}
                  </Tab>
                  <Tab
                    id={"cssv2Item"}
                    link={`${url}/severity`}
                    tooltip={t("searchFindings.tabSeverity.tooltip")}
                  >
                    {t("searchFindings.tabSeverity.tabTitle")}
                  </Tab>
                  <Tab
                    id={"evidenceItem"}
                    link={`${url}/evidence`}
                    tooltip={t("searchFindings.tabEvidence.tooltip")}
                  >
                    {t("searchFindings.tabEvidence.tabTitle")}
                  </Tab>
                  <Tab
                    id={"trackingItem"}
                    link={`${url}/tracking`}
                    tooltip={t("searchFindings.tabTracking.tooltip")}
                  >
                    {t("searchFindings.tabTracking.tabTitle")}
                  </Tab>
                  <Tab
                    id={"recordsItem"}
                    link={`${url}/records`}
                    tooltip={t("searchFindings.tabRecords.tooltip")}
                  >
                    {t("searchFindings.tabRecords.tabTitle")}
                  </Tab>
                  {headerData.finding.hacker === "machine@fluidattacks.com" ? (
                    <Can do={"api_resolvers_finding_machine_jobs_resolve"}>
                      <Tab
                        id={"machineItem"}
                        link={`${url}/machine`}
                        tooltip={t("searchFindings.tabMachine.tooltip")}
                      >
                        {t("searchFindings.tabMachine.tabTitle")}
                      </Tab>
                    </Can>
                  ) : undefined}
                  {isDraft ? undefined : (
                    <Can do={"api_resolvers_finding_consulting_resolve"}>
                      <Tab
                        id={"commentItem"}
                        link={`${url}/consulting`}
                        tooltip={t("searchFindings.tabComments.tooltip")}
                      >
                        {t("searchFindings.tabComments.tabTitle")}
                      </Tab>
                    </Can>
                  )}
                  <Can do={"api_resolvers_finding_observations_resolve"}>
                    <Tab
                      id={"observationsItem"}
                      link={`${url}/observations`}
                      tooltip={t("searchFindings.tabObservations.tooltip")}
                    >
                      {t("searchFindings.tabObservations.tabTitle")}
                    </Tab>
                  </Can>
                </Tabs>
              </div>
              <TabContent>
                <Switch>
                  <Route
                    exact={true}
                    path={`${path}/locations/:vulnerabilityId?`}
                  >
                    <VulnsView refetchFindingHeader={refetchFindingHeader} />
                  </Route>
                  <Route
                    component={DescriptionView}
                    exact={true}
                    path={`${path}/description`}
                  />
                  <Route
                    component={SeverityView}
                    exact={true}
                    path={`${path}/severity`}
                  />
                  <Route
                    component={EvidenceView}
                    exact={true}
                    path={`${path}/evidence`}
                  />
                  <Route
                    component={MachineView}
                    exact={true}
                    path={`${path}/machine`}
                  />
                  <Route
                    component={TrackingView}
                    exact={true}
                    path={`${path}/tracking`}
                  />
                  <Route
                    component={RecordsView}
                    exact={true}
                    path={`${path}/records`}
                  />
                  <Route
                    component={CommentsView}
                    exact={true}
                    path={`${path}/:type(consulting|observations)`}
                  />
                  <Redirect to={`${path}/locations`} />
                </Switch>
              </TabContent>
            </div>
          </div>
        </div>
      </div>
      <Modal
        onClose={closeDeleteModal}
        open={isDeleteModalOpen}
        title={t("searchFindings.delete.title")}
      >
        <Formik
          enableReinitialize={true}
          initialValues={{}}
          name={"removeFinding"}
          onSubmit={handleDelete}
          validationSchema={validations}
        >
          <Form id={"removeFinding"}>
            <FormGroup>
              <Select
                label={t("searchFindings.delete.justif.label")}
                name={"justification"}
              >
                <option value={""} />
                <option value={"DUPLICATED"}>
                  {t("searchFindings.delete.justif.duplicated")}
                </option>
                <option value={"FALSE_POSITIVE"}>
                  {t("searchFindings.delete.justif.falsePositive")}
                </option>
                <option value={"NOT_REQUIRED"}>
                  {t("searchFindings.delete.justif.notRequired")}
                </option>
              </Select>
            </FormGroup>
            <ModalConfirm disabled={deleting} onCancel={closeDeleteModal} />
          </Form>
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { FindingContent };
