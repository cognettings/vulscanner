import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type { ColumnDef } from "@tanstack/react-table";
import dayjs from "dayjs";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, {
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import { useTranslation } from "react-i18next";
import { useLocation, useParams } from "react-router-dom";

import {
  areAllSuccessful,
  handleCloseVulnerabilities,
  resubmitVulnerabilityProps,
} from "./helpers";

import type { IConfirmFn } from "components/ConfirmDialog";
import type { IFilter, IPermanentData } from "components/Filter";
import { Filters, useFilters } from "components/Filter";
import { Col } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import { filterDate } from "components/Table/filters/filterFunctions/filterDate";
import { includeTagsFormatter } from "components/Table/formatters/includeTagsFormatter";
import type { ICellHelper } from "components/Table/types";
import { Can } from "context/authz/Can";
import { authzPermissionsContext } from "context/authz/config";
import { Have } from "context/authz/Have";
import { meetingModeContext } from "context/meetingMode";
import { useStoredState } from "hooks";
import { GET_ME_VULNERABILITIES_ASSIGNED_IDS } from "pages/home/dashboard/navbar/to-do/queries";
import { ExpertButton } from "scenes/Dashboard/components/ExpertButton";
import { UpdateVerificationModal } from "scenes/Dashboard/components/UpdateVerificationModal";
import { VulnComponent } from "scenes/Dashboard/components/Vulnerabilities";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter";
import { techniqueFormatter } from "scenes/Dashboard/components/Vulnerabilities/TechFormatter/index";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { UpdateDescription } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription";
import { UpdateSeverity } from "scenes/Dashboard/components/Vulnerabilities/UpdateSeverity";
import { UploadVulnerabilities } from "scenes/Dashboard/components/Vulnerabilities/uploadFile";
import {
  filterOutVulnerabilities,
  filterZeroRisk,
  formatVulnerabilities,
  formatVulnerabilitiesTreatment,
  getNonSelectableVulnerabilitiesOnCloseIds,
  getNonSelectableVulnerabilitiesOnReattackIds,
  getNonSelectableVulnerabilitiesOnResubmitIds,
  getNonSelectableVulnerabilitiesOnVerifyIds,
} from "scenes/Dashboard/components/Vulnerabilities/utils";
import { ActionButtons } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/ActionButtons";
import { HandleAcceptanceModal } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/HandleAcceptanceModal";
import {
  CLOSE_VULNERABILITIES,
  GET_FINDING_INFO,
  GET_FINDING_NZR_VULNS,
  GET_FINDING_VULN_DRAFTS,
  GET_FINDING_ZR_VULNS,
  RESUBMIT_VULNERABILITIES,
  SEND_VULNERABILITY_NOTIFICATION,
} from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/queries";
import type {
  ICloseVulnerabilitiesResultAttr,
  IGetFindingAndGroupInfo,
  IModalConfig,
  ISendNotificationResultAttr,
  IVulnerabilitiesConnection,
  IVulnerabilityEdge,
} from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/types";
import {
  filterVerification,
  getRejectedVulns,
  getRequestedZeroRiskVulns,
  getSubmittedVulns,
  getVulnsPendingOfAcceptance,
  getVunerableLocations,
} from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/utils";
import { getCVSSF, getRiskExposure } from "utils/cvss";
import { severityFormatter } from "utils/formatHelpers";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IVulnsViewProps {
  refetchFindingHeader: () => void;
}

export const VulnsView: React.FC<IVulnsViewProps> = ({
  refetchFindingHeader,
}: IVulnsViewProps): JSX.Element => {
  const { findingId, groupName } = useParams<{
    findingId: string;
    groupName: string;
  }>();
  const { t } = useTranslation();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canRetrieveDrafts: boolean = permissions.can(
    "api_resolvers_finding_drafts_connection_resolve"
  );
  const canRetrieveZeroRisk: boolean = permissions.can(
    "api_resolvers_finding_zero_risk_connection_resolve"
  );
  const { meetingMode } = useContext(meetingModeContext);
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);

  const rootFilter = searchParams.get("location") ?? "";

  const [isOpen, setIsOpen] = useState(false);

  const [isHandleAcceptanceModalOpen, setIsHandleAcceptanceModalOpen] =
    useState(false);
  const toggleHandleAcceptanceModal = useCallback((): void => {
    setIsHandleAcceptanceModalOpen(!isHandleAcceptanceModalOpen);
  }, [isHandleAcceptanceModalOpen]);
  const [remediationModal, setRemediationModal] = useState<IModalConfig>({
    clearSelected: (): void => undefined,
    selectedVulnerabilities: [],
  });
  const openRemediationModal = useCallback(
    (
      selectedVulnerabilities: IVulnRowAttr[],
      clearSelected: () => void
    ): void => {
      setRemediationModal({ clearSelected, selectedVulnerabilities });
    },
    []
  );
  const closeRemediationModal = useCallback((): void => {
    setIsOpen(false);
  }, []);
  const [isEditing, setIsEditing] = useState(false);
  const toggleEdit = useCallback((): void => {
    setIsEditing(!isEditing);
  }, [isEditing]);
  const handleCloseUpdateModal = useCallback((): void => {
    setIsEditing(false);
  }, []);
  const [isNotify, setIsNotify] = useState(false);
  const toggleNotify = useCallback((): void => {
    setIsNotify(!isNotify);
  }, [isNotify]);
  const handleCloseNotifyModal = useCallback((): void => {
    setIsNotify(false);
  }, []);
  const [isRequestingVerify, setIsRequestingVerify] = useState(false);
  const [isVerifying, setIsVerifying] = useState(false);
  const [isResubmitting, setIsResubmitting] = useState(false);
  const [isClosing, setIsClosing] = useState(false);
  const [isUpdatingSeverity, setIsUpdatingSeverity] = useState(false);
  const closeSeverityModal = useCallback((): void => {
    setIsUpdatingSeverity(false);
    setRemediationModal({
      clearSelected: (): void => undefined,
      selectedVulnerabilities: [],
    });
  }, []);
  const toggleUpdateSeverity = useCallback((): void => {
    setIsUpdatingSeverity(!isUpdatingSeverity);
  }, [isUpdatingSeverity]);

  const { data, refetch: refetchFindingAndGroup } =
    useQuery<IGetFindingAndGroupInfo>(GET_FINDING_INFO, {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred loading finding", error);
        });
      },
      variables: {
        findingId,
      },
    });

  const {
    data: nzrVulnsData,
    fetchMore: nzrFetchMore,
    refetch: nzrRefetch,
  } = useQuery<{
    finding: { vulnerabilitiesConnection: IVulnerabilitiesConnection };
  }>(GET_FINDING_NZR_VULNS, {
    fetchPolicy: "network-only",
    nextFetchPolicy: "cache-first",
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred loading finding non zero risk vulnerabilities",
          error
        );
      });
    },
    variables: {
      findingId,
      first: 100,
    },
  });
  const vulnerabilitiesConnection =
    nzrVulnsData === undefined
      ? undefined
      : nzrVulnsData.finding.vulnerabilitiesConnection;

  const nzrVulnsPageInfo =
    vulnerabilitiesConnection === undefined
      ? undefined
      : vulnerabilitiesConnection.pageInfo;
  const nzrVulnsEdges: IVulnerabilityEdge[] = useMemo(
    (): IVulnerabilityEdge[] =>
      vulnerabilitiesConnection === undefined
        ? []
        : vulnerabilitiesConnection.edges,
    [vulnerabilitiesConnection]
  );
  const {
    data: vulnDraftsData,
    fetchMore: vulnDraftsFetchMore,
    refetch: vulnDraftsRefetch,
  } = useQuery<{
    finding: { draftsConnection: IVulnerabilitiesConnection | undefined };
  }>(GET_FINDING_VULN_DRAFTS, {
    fetchPolicy: "network-only",
    nextFetchPolicy: "cache-first",
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred loading finding vulnerability drafts",
          error
        );
      });
    },
    variables: {
      canRetrieveDrafts,
      findingId,
      first: 100,
    },
  });
  const vulnDraftsConnection =
    vulnDraftsData === undefined
      ? undefined
      : vulnDraftsData.finding.draftsConnection;
  const vulnDraftsPageInfo =
    vulnDraftsConnection === undefined
      ? undefined
      : vulnDraftsConnection.pageInfo;
  const vulnDraftsEdges: IVulnerabilityEdge[] =
    vulnDraftsConnection === undefined ? [] : vulnDraftsConnection.edges;
  const {
    data: zrVulnsData,
    fetchMore: zrFetchMore,
    refetch: zrRefetch,
  } = useQuery<{
    finding: { zeroRiskConnection: IVulnerabilitiesConnection | undefined };
  }>(GET_FINDING_ZR_VULNS, {
    fetchPolicy: "network-only",
    nextFetchPolicy: "cache-first",
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred loading finding zero risk vulnerabilities",
          error
        );
      });
    },
    variables: {
      canRetrieveZeroRisk,
      findingId,
      first: 100,
    },
  });
  const zeroRiskConnection =
    zrVulnsData === undefined
      ? undefined
      : zrVulnsData.finding.zeroRiskConnection;
  const zrVulnsPageInfo =
    zeroRiskConnection === undefined ? undefined : zeroRiskConnection.pageInfo;
  const zrVulnsEdges: IVulnerabilityEdge[] =
    zeroRiskConnection === undefined ? [] : zeroRiskConnection.edges;

  const unformattedVulns: IVulnRowAttr[] = zrVulnsEdges
    .concat(nzrVulnsEdges)
    .concat(vulnDraftsEdges)
    .map(
      (vulnerabilityEdge: IVulnerabilityEdge): IVulnRowAttr =>
        vulnerabilityEdge.node
    );

  const vulnerabilities: IVulnRowAttr[] = formatVulnerabilitiesTreatment({
    organizationsGroups: undefined,
    vulnerabilities: unformattedVulns.map(
      (vulnerability: IVulnRowAttr): IVulnRowAttr => ({
        ...vulnerability,
        groupName,
        where:
          vulnerability.vulnerabilityType === "lines" &&
          vulnerability.rootNickname !== null &&
          vulnerability.rootNickname !== "" &&
          !vulnerability.where.startsWith(`${vulnerability.rootNickname}/`)
            ? `${vulnerability.rootNickname}/${vulnerability.where}`
            : vulnerability.where,
      })
    ),
  });

  const [filters, setFilters] = useState<IFilter<IVulnRowAttr>[]>([
    {
      id: "where",
      key: "where",
      label: "Location",
      type: "text",
      value: rootFilter,
    },
    {
      id: "currentState",
      key: "state",
      label: t("searchFindings.tabVuln.vulnTable.status"),
      selectOptions: [
        { header: t("searchFindings.tabVuln.open"), value: "VULNERABLE" },
        { header: t("searchFindings.tabVuln.closed"), value: "SAFE" },
        { header: t("searchFindings.tabVuln.rejected"), value: "REJECTED" },
        { header: t("searchFindings.tabVuln.submitted"), value: "SUBMITTED" },
      ],
      type: "select",
      value: "VULNERABLE",
    },
    {
      id: "reportDate",
      key: "reportDate",
      label: t("searchFindings.tabVuln.vulnTable.reportDate"),
      type: "dateRange",
    },
    {
      id: "verification",
      key: filterVerification,
      label: t("searchFindings.tabVuln.vulnTable.reattack"),
      selectOptions: [
        { header: t("searchFindings.tabVuln.onHold"), value: "On_hold" },
        {
          header: t("searchFindings.tabVuln.requested"),
          value: "Requested",
        },
        {
          header: t("searchFindings.tabVuln.verified"),
          value: "Verified",
        },
        {
          header: t("searchFindings.tabVuln.notRequested"),
          value: "NotRequested",
        },
      ],
      type: "select",
    },
    {
      id: "treatment",
      key: (vuln, value): boolean => {
        if (_.isEmpty(value)) return true;
        const formattedvuln = formatVulnerabilities({
          vulnerabilities: [vuln],
        });

        return formattedvuln[0].treatmentStatus === value;
      },
      label: t("searchFindings.tabVuln.vulnTable.treatment"),
      selectOptions: [
        "-",
        String(t("searchFindings.tabDescription.treatment.new")),
        String(t("searchFindings.tabDescription.treatment.inProgress")),
        String(t("searchFindings.tabDescription.treatment.accepted")),
        String(t("searchFindings.tabDescription.treatment.acceptedUndefined")),
      ],
      type: "select",
    },
    {
      id: "tag",
      key: "tag",
      label: t("searchFindings.tabVuln.vulnTable.tags"),
      type: "text",
    },
    {
      id: "treatmentAssigned",
      key: "treatmentAssigned",
      label: "Assignees",
      selectOptions: (vulns: IVulnRowAttr[]): string[] =>
        [
          ...new Set(vulns.map((vuln): string => vuln.treatmentAssigned ?? "")),
        ].filter(Boolean),
      type: "select",
    },
  ]);

  const [filterVal, setFilterVal] = useStoredState<IPermanentData[]>(
    "vulnerabilitiesTableFilters",
    [
      { id: "currentState", value: "" },
      { id: "reportDate", rangeValues: ["", ""] },
      { id: "verification", value: "" },
      { id: "treatment", value: "" },
      { id: "tag", value: "" },
      { id: "treatmentAssigned", value: "" },
    ],
    localStorage
  );

  const meetingVulnerabilities = meetingMode
    ? vulnerabilities.filter((vulnerability: IVulnRowAttr): boolean =>
        ["VULNERABLE", "SAFE"].includes(vulnerability.state)
      )
    : vulnerabilities;
  const filteredVulnerabilities = useFilters(meetingVulnerabilities, filters);

  const [sendNotification, { loading }] =
    useMutation<ISendNotificationResultAttr>(SEND_VULNERABILITY_NOTIFICATION, {
      onCompleted: (result: ISendNotificationResultAttr): void => {
        if (result.sendVulnerabilityNotification.success) {
          msgSuccess(
            t("searchFindings.tabDescription.notify.emailNotificationText"),
            t("searchFindings.tabDescription.notify.emailNotificationTitle")
          );
        }
      },
      onError: (updateError: ApolloError): void => {
        updateError.graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(
            t("searchFindings.tabDescription.notify.emailNotificationError")
          );
          Logger.warning("An error occurred sending the notification", error);
        });
      },
    });
  const handleSendNotification = useCallback(async (): Promise<void> => {
    await sendNotification({
      variables: {
        findingId,
      },
    });
    setIsNotify(false);
  }, [findingId, sendNotification]);

  const toggleRequestVerify = useCallback((): void => {
    if (isRequestingVerify) {
      setIsRequestingVerify(!isRequestingVerify);
    } else {
      const { selectedVulnerabilities } = remediationModal;
      const newVulnerabilities: IVulnRowAttr[] = filterOutVulnerabilities(
        selectedVulnerabilities,
        filterZeroRisk(vulnerabilities),
        getNonSelectableVulnerabilitiesOnReattackIds
      );
      if (selectedVulnerabilities.length > newVulnerabilities.length) {
        setIsRequestingVerify(!isRequestingVerify);
        if (newVulnerabilities.length === 0) {
          msgError(t("searchFindings.tabVuln.errors.selectedVulnerabilities"));
        } else {
          setRemediationModal(
            (currentRemediation): IModalConfig => ({
              clearSelected: currentRemediation.clearSelected,
              selectedVulnerabilities: newVulnerabilities,
            })
          );
          setIsOpen(true);
        }
      } else if (selectedVulnerabilities.length > 0) {
        setIsOpen(true);
        setIsRequestingVerify(!isRequestingVerify);
      } else {
        setIsRequestingVerify(!isRequestingVerify);
      }
    }
  }, [isRequestingVerify, remediationModal, t, vulnerabilities]);

  const toggleVerify = useCallback((): void => {
    if (isVerifying) {
      setIsVerifying(!isVerifying);
    } else {
      const { selectedVulnerabilities } = remediationModal;
      const newVulnerabilities: IVulnRowAttr[] = filterOutVulnerabilities(
        selectedVulnerabilities,
        filterZeroRisk(vulnerabilities),
        getNonSelectableVulnerabilitiesOnVerifyIds
      );
      if (selectedVulnerabilities.length > newVulnerabilities.length) {
        setIsVerifying(!isVerifying);
        if (newVulnerabilities.length === 0) {
          msgError(t("searchFindings.tabVuln.errors.selectedVulnerabilities"));
        } else {
          setRemediationModal(
            (currentRemediation): IModalConfig => ({
              clearSelected: currentRemediation.clearSelected,
              selectedVulnerabilities: newVulnerabilities,
            })
          );
          setIsOpen(true);
        }
      } else if (selectedVulnerabilities.length > 0) {
        setIsOpen(true);
        setIsVerifying(!isVerifying);
      } else {
        setIsVerifying(!isVerifying);
      }
    }
  }, [isVerifying, remediationModal, t, vulnerabilities]);

  const refetchVulnsData = useCallback((): void => {
    void nzrRefetch();
    void vulnDraftsRefetch();
    void zrRefetch();
  }, [nzrRefetch, vulnDraftsRefetch, zrRefetch]);
  const [resubmitVulnerability] = useMutation(
    RESUBMIT_VULNERABILITIES,
    resubmitVulnerabilityProps(groupName, findingId, refetchVulnsData)
  );
  const [closeVulnerabilities, { client }] =
    useMutation<ICloseVulnerabilitiesResultAttr>(CLOSE_VULNERABILITIES);
  const handleResubmit = useCallback(async (): Promise<void> => {
    const { selectedVulnerabilities } = remediationModal;
    const newVulnerabilities: IVulnRowAttr[] = filterOutVulnerabilities(
      selectedVulnerabilities,
      filterZeroRisk(vulnerabilities),
      getNonSelectableVulnerabilitiesOnResubmitIds
    );
    if (selectedVulnerabilities.length !== newVulnerabilities.length) {
      msgError(t("searchFindings.tabVuln.errors.selectedVulnerabilities"));
    }
    if (
      selectedVulnerabilities.length > 0 &&
      selectedVulnerabilities.length === newVulnerabilities.length
    ) {
      const selectedVulnerabilitiesIds = newVulnerabilities.map(
        (vuln: IVulnRowAttr): string => vuln.id
      );
      await resubmitVulnerability({
        variables: {
          findingId,
          vulnerabilities: selectedVulnerabilitiesIds,
        },
      });
      setIsResubmitting(false);
    } else {
      setIsResubmitting(true);
      setRemediationModal(
        (currentRemediation): IModalConfig => ({
          clearSelected: currentRemediation.clearSelected,
          selectedVulnerabilities: newVulnerabilities,
        })
      );
    }
  }, [findingId, remediationModal, resubmitVulnerability, t, vulnerabilities]);

  const handleCancelAction = useCallback((): void => {
    setIsResubmitting(false);
    setIsClosing(false);
  }, []);

  const onCloseVulnerabilitiesAux = useCallback(
    async (newVulnerabilities: IVulnRowAttr[]): Promise<void> => {
      try {
        const results = await handleCloseVulnerabilities(
          closeVulnerabilities,
          newVulnerabilities
        );
        const areAllMutationValid = areAllSuccessful(results);
        if (areAllMutationValid.every(Boolean)) {
          refetchFindingHeader();
          refetchVulnsData();
          msgSuccess(
            t("groupAlerts.closedVulnerabilitySuccess"),
            t("groupAlerts.updatedTitle")
          );
          remediationModal.clearSelected();
          await refetchFindingAndGroup();
        }
      } catch (requestError: unknown) {
        (requestError as ApolloError).graphQLErrors.forEach((error): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred closing vulnerabilities", error);
        });
      } finally {
        void client.refetchQueries({
          include: [GET_ME_VULNERABILITIES_ASSIGNED_IDS],
        });
      }
    },
    [
      client,
      closeVulnerabilities,
      refetchFindingHeader,
      refetchFindingAndGroup,
      refetchVulnsData,
      remediationModal,
      t,
    ]
  );

  const onCloseVulnerabilities = useCallback(
    (confirm: IConfirmFn): (() => void) =>
      (): void => {
        const { selectedVulnerabilities } = remediationModal;
        const newVulnerabilities: IVulnRowAttr[] = filterOutVulnerabilities(
          selectedVulnerabilities,
          filterZeroRisk(vulnerabilities),
          getNonSelectableVulnerabilitiesOnCloseIds
        );
        if (selectedVulnerabilities.length !== newVulnerabilities.length) {
          msgError(t("searchFindings.tabVuln.errors.selectedVulnerabilities"));
        }
        if (
          selectedVulnerabilities.length > 0 &&
          selectedVulnerabilities.length === newVulnerabilities.length
        ) {
          confirm((): void => {
            void onCloseVulnerabilitiesAux(newVulnerabilities);
          });
          setIsClosing(false);
        } else {
          setIsClosing(true);
          setRemediationModal(
            (currentRemediation): IModalConfig => ({
              clearSelected: currentRemediation.clearSelected,
              selectedVulnerabilities: newVulnerabilities,
            })
          );
        }
      },
    [onCloseVulnerabilitiesAux, remediationModal, t, vulnerabilities]
  );

  const toggleModal = useCallback((): void => {
    setIsOpen(true);
  }, []);

  useEffect((): void => {
    if (!_.isUndefined(nzrVulnsPageInfo)) {
      if (nzrVulnsPageInfo.hasNextPage) {
        void nzrFetchMore({
          variables: { after: nzrVulnsPageInfo.endCursor, first: 1200 },
        });
      }
    }
  }, [nzrVulnsPageInfo, nzrFetchMore]);
  useEffect((): void => {
    if (!_.isUndefined(vulnDraftsPageInfo)) {
      if (vulnDraftsPageInfo.hasNextPage) {
        void vulnDraftsFetchMore({
          variables: { after: vulnDraftsPageInfo.endCursor, first: 1200 },
        });
      }
    }
  }, [vulnDraftsPageInfo, vulnDraftsFetchMore]);
  useEffect((): void => {
    if (!_.isUndefined(zrVulnsPageInfo)) {
      if (zrVulnsPageInfo.hasNextPage) {
        void zrFetchMore({
          variables: { after: zrVulnsPageInfo.endCursor, first: 1200 },
        });
      }
    }
  }, [zrVulnsPageInfo, zrFetchMore]);

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.StrictMode />;
  }

  const isFindingReleased: boolean = !_.isEmpty(data.finding.releaseDate);

  const columns: ColumnDef<IVulnRowAttr>[] = [
    {
      accessorKey: "where",
      cell: (cell: ICellHelper<IVulnRowAttr>): JSX.Element | string => {
        const vuln: IVulnRowAttr = cell.row.original;
        const daysFromReport = dayjs().diff(vuln.reportDate, "days");

        return includeTagsFormatter({
          newTag: daysFromReport <= 7 && vuln.state === "VULNERABLE",
          text: vuln.advisories
            ? `${vuln.where} (${vuln.advisories.package}, ${vuln.advisories.vulnerableVersion})`
            : vuln.where,
        });
      },
      enableColumnFilter: false,
      header: t("searchFindings.tabVuln.vulnTable.where"),
    },
    {
      accessorKey: "specific",
      enableColumnFilter: false,
      header: t("searchFindings.tabVuln.vulnTable.specific"),
      sortingFn: "alphanumeric",
    },
    {
      accessorKey: "state",
      cell: (cell): JSX.Element => {
        const labels: Record<string, string> = {
          REJECTED: t("searchFindings.tabVuln.rejected"),
          SAFE: t("searchFindings.tabVuln.closed"),
          SUBMITTED: t("searchFindings.tabVuln.submitted"),
          VULNERABLE: t("searchFindings.tabVuln.open"),
        };

        return statusFormatter(labels[cell.getValue<string>()]);
      },
      header: t("searchFindings.tabVuln.vulnTable.status"),
      meta: { filterType: "select" },
    },
    {
      accessorKey: "technique",
      cell: (cell): JSX.Element => {
        const labels: Record<string, string> = {
          CSPM: t("searchFindings.tabVuln.technique.cspm"),
          DAST: t("searchFindings.tabVuln.technique.dast"),
          MPT: t("searchFindings.tabVuln.technique.mpt"),
          RE: t("searchFindings.tabVuln.technique.re"),
          SAST: t("searchFindings.tabVuln.technique.sast"),
          SCA: t("searchFindings.tabVuln.technique.sca"),
          SCR: t("searchFindings.tabVuln.technique.scr"),
        };

        return techniqueFormatter(labels[cell.getValue<string>()]);
      },
      header: t("searchFindings.tabVuln.vulnTable.technique"),
      meta: { filterType: "select" },
    },
    {
      accessorKey: "severityTemporalScore",
      cell: (cell: ICellHelper<IVulnRowAttr>): JSX.Element =>
        severityFormatter(cell.getValue()),
      header: t("searchFindings.tabVuln.vulnTable.severity"),
    },
    {
      accessorFn: (row: IVulnRowAttr): string => {
        return getRiskExposure(
          getCVSSF(row.severityTemporalScore),
          data.finding.totalOpenCVSSF,
          row.state
        );
      },
      header: t("searchFindings.tabVuln.vulnTable.riskExposure"),
      id: "riskExposureColumn",
    },
    {
      accessorKey: "reportDate",
      filterFn: filterDate,
      header: t("searchFindings.tabVuln.vulnTable.reportDate"),
      meta: { filterType: "dateRange" },
    },
    {
      accessorKey: "verification",
      cell: (cell: ICellHelper<IVulnRowAttr>): string => {
        if (cell.getValue() === "On_hold") {
          return t("searchFindings.tabVuln.onHold");
        }

        return cell.getValue();
      },

      header: t("searchFindings.tabVuln.vulnTable.reattack"),
      meta: { filterType: "select" },
    },
    {
      accessorKey: "treatmentStatus",
      header: t("searchFindings.tabVuln.vulnTable.treatment"),
      meta: { filterType: "select" },
    },
    {
      accessorKey: "tag",
      header: t("searchFindings.tabVuln.vulnTable.tags"),
    },
    {
      accessorKey: "treatmentAcceptanceStatus",
      header: t("searchFindings.tabVuln.vulnTable.treatmentAcceptance"),
      meta: { filterType: "select" },
    },
    {
      accessorKey: "treatmentAssigned",
      header: t("searchFindings.tabVuln.vulnTable.treatmentAssigned"),
      meta: { filterType: "select" },
    },
  ];

  return (
    <React.StrictMode>
      <React.Fragment>
        <div>
          <div>
            <div>
              <VulnComponent
                columns={columns}
                enableColumnFilters={false}
                extraButtons={
                  <ActionButtons
                    areRejectedVulns={
                      getRejectedVulns(vulnerabilities).length > 0
                    }
                    areRequestedZeroRiskVulns={
                      getRequestedZeroRiskVulns(vulnerabilities).length > 0
                    }
                    areSubmittedVulns={
                      getSubmittedVulns(vulnerabilities).length > 0
                    }
                    areVulnerableLocations={
                      getVunerableLocations(
                        nzrVulnsEdges.map(
                          (
                            vulnerabilityEdge: IVulnerabilityEdge
                          ): IVulnRowAttr => vulnerabilityEdge.node
                        )
                      ).length > 0
                    }
                    areVulnsPendingOfAcceptance={
                      getVulnsPendingOfAcceptance(vulnerabilities).length > 0
                    }
                    areVulnsSelected={
                      remediationModal.selectedVulnerabilities.length > 0
                    }
                    isClosing={isClosing}
                    isEditing={isEditing}
                    isFindingReleased={isFindingReleased}
                    isOpen={isOpen}
                    isRequestingReattack={isRequestingVerify}
                    isResubmitting={isResubmitting}
                    isVerified={data.finding.verified}
                    isVerifying={isVerifying}
                    onCancel={handleCancelAction}
                    onClosing={onCloseVulnerabilities}
                    onEdit={toggleEdit}
                    onNotify={toggleNotify}
                    onRequestReattack={toggleRequestVerify}
                    onResubmit={handleResubmit}
                    onUpdateSeverity={toggleUpdateSeverity}
                    onVerify={toggleVerify}
                    openHandleAcceptance={toggleHandleAcceptanceModal}
                    openModal={toggleModal}
                    status={data.finding.status}
                  />
                }
                filters={
                  <Filters
                    dataset={vulnerabilities}
                    filters={filters}
                    permaset={[filterVal, setFilterVal]}
                    setFilters={setFilters}
                  />
                }
                findingState={data.finding.status}
                id={"vulnsView"}
                isClosing={isClosing}
                isEditing={isEditing}
                isFindingReleased={isFindingReleased}
                isRequestingReattack={isRequestingVerify}
                isResubmitting={isResubmitting}
                isUpdatingSeverity={isUpdatingSeverity}
                isVerifyingRequest={isVerifying}
                onVulnSelect={openRemediationModal}
                refetchData={refetchVulnsData}
                vulnerabilities={filterZeroRisk(filteredVulnerabilities)}
              />
            </div>
            <br />
            <Col>
              <Have I={"can_report_vulnerabilities"}>
                <Can do={"api_mutations_upload_file_mutate"}>
                  <UploadVulnerabilities
                    findingId={findingId}
                    groupName={groupName}
                    refetchData={refetchVulnsData}
                  />
                </Can>
              </Have>
            </Col>
          </div>
        </div>
        {isOpen && (
          <UpdateVerificationModal
            clearSelected={_.get(remediationModal, "clearSelected")}
            handleCloseModal={closeRemediationModal}
            isReattacking={isRequestingVerify}
            isVerifying={isVerifying}
            refetchData={refetchVulnsData}
            refetchFindingAndGroup={refetchFindingAndGroup}
            refetchFindingHeader={refetchFindingHeader}
            setRequestState={toggleRequestVerify}
            setVerifyState={toggleVerify}
            vulns={remediationModal.selectedVulnerabilities}
          />
        )}
        {isHandleAcceptanceModalOpen && (
          <HandleAcceptanceModal
            findingId={findingId}
            groupName={groupName}
            handleCloseModal={toggleHandleAcceptanceModal}
            refetchData={refetchVulnsData}
            vulns={vulnerabilities}
          />
        )}
        {isEditing && (
          <Modal
            onClose={handleCloseUpdateModal}
            open={isEditing}
            title={t("searchFindings.tabDescription.editVuln")}
          >
            <UpdateDescription
              findingId={findingId}
              groupName={groupName}
              handleClearSelected={_.get(remediationModal, "clearSelected")}
              handleCloseModal={handleCloseUpdateModal}
              refetchData={refetchVulnsData}
              vulnerabilities={remediationModal.selectedVulnerabilities}
            />
          </Modal>
        )}
        {isNotify && (
          <Modal
            onClose={handleCloseNotifyModal}
            open={isNotify}
            title={t("searchFindings.notifyModal.body")}
          >
            <ModalConfirm
              disabled={loading}
              onCancel={handleCloseNotifyModal}
              onConfirm={handleSendNotification}
              txtCancel={t("searchFindings.notifyModal.cancel")}
              txtConfirm={t("searchFindings.notifyModal.notify")}
            />
          </Modal>
        )}
        {isUpdatingSeverity && (
          <Modal
            minWidth={700}
            onClose={closeSeverityModal}
            open={isUpdatingSeverity}
            title={t("searchFindings.tabDescription.updateVulnSeverity")}
          >
            <UpdateSeverity
              findingId={findingId}
              handleCloseModal={closeSeverityModal}
              refetchData={refetchVulnsData}
              vulnerabilities={remediationModal.selectedVulnerabilities}
            />
          </Modal>
        )}
        <ExpertButton />
      </React.Fragment>
    </React.StrictMode>
  );
};
