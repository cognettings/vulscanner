/* eslint fp/no-mutation: 0 */
import { useQuery } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import _ from "lodash";
import React, { useCallback, useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import {
  GET_GROUP_VULNERABILITIES,
  GET_GROUP_VULNERABILITY_DRAFTS,
} from "./queries";
import { tableColumns, tableFilters } from "./tableUtils";
import type { IGroupVulnerabilities, IGroupVulnerabilityDrafts } from "./types";
import {
  formatVulnAttribute,
  formatVulnerability,
  formatVulnerabilityDrafts,
} from "./utils";

import type {
  IVulnerabilityCriteriaData,
  IVulnerabilityCriteriaRequirement,
} from "../../Finding-Content/DescriptionView/types";
import {
  getRequerimentsData,
  getVulnerabilitiesCriteriaData,
} from "../../Finding-Content/DescriptionView/utils";
import { ActionButtons } from "../../Finding-Content/VulnerabilitiesView/ActionButtons";
import { HandleAcceptanceModal } from "../../Finding-Content/VulnerabilitiesView/HandleAcceptanceModal";
import type { IModalConfig } from "../../Finding-Content/VulnerabilitiesView/types";
import {
  getRequestedZeroRiskVulns,
  getSubmittedVulns,
} from "../../Finding-Content/VulnerabilitiesView/utils";
import type { IFilter } from "components/Filter";
import { Filters, useFilters } from "components/Filter";
import { Modal } from "components/Modal";
import { authzPermissionsContext } from "context/authz/config";
import { useDebouncedCallback, useStoredState } from "hooks";
import { UpdateVerificationModal } from "scenes/Dashboard/components/UpdateVerificationModal";
import { VulnComponent } from "scenes/Dashboard/components/Vulnerabilities";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { UpdateDescription } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription";
import {
  filterOutVulnerabilities,
  filterZeroRisk,
  getNonSelectableVulnerabilitiesOnReattackIds,
  getNonSelectableVulnerabilitiesOnVerifyIds,
} from "scenes/Dashboard/components/Vulnerabilities/utils";
import { msgError } from "utils/notifications";

const GroupVulnerabilitiesView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const { t } = useTranslation();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canRetrieveDrafts: boolean = permissions.can(
    "api_resolvers_group_vulnerability_drafts_resolve"
  );
  const [remediationModal, setRemediationModal] = useState<IModalConfig>({
    clearSelected: (): void => undefined,
    selectedVulnerabilities: [],
  });
  const [vulnFilters, setVulnFilters] = useStoredState<IFilter<IVulnRowAttr>[]>(
    "vulnerabilitiesTable-columnFilters",
    tableFilters
  );
  const [isRequestingVerify, setIsRequestingVerify] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [vulnData, setVulnData] = useState<
    Record<string, IVulnerabilityCriteriaData> | undefined
  >();
  const [requirementData, setRequirementData] = useState<
    Record<string, IVulnerabilityCriteriaRequirement> | undefined
  >();

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

  const [isVerifying, setIsVerifying] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const toggleEdit = useCallback((): void => {
    setIsEditing(!isEditing);
  }, [isEditing]);

  const handleCloseUpdateModal = useCallback((): void => {
    setIsEditing(false);
  }, []);

  const [isHandleAcceptanceModalOpen, setIsHandleAcceptanceModalOpen] =
    useState(false);
  const toggleHandleAcceptanceModal = useCallback((): void => {
    setIsHandleAcceptanceModalOpen(!isHandleAcceptanceModalOpen);
  }, [isHandleAcceptanceModalOpen]);

  // GraphQL operations
  const { data: vulnsZeroRisk } = useQuery<IGroupVulnerabilities>(
    GET_GROUP_VULNERABILITIES,
    {
      fetchPolicy: "no-cache",
      variables: { first: 100, groupName, zeroRisk: "REQUESTED" },
    }
  );

  const { data, fetchMore, refetch } = useQuery<IGroupVulnerabilities>(
    GET_GROUP_VULNERABILITIES,
    {
      fetchPolicy: "cache-first",
      variables: { first: 150, groupName, search: "" },
    }
  );

  const {
    data: vulnDraftsData,
    fetchMore: vulnDraftsFetchMore,
    refetch: vulnDraftsRefetch,
  } = useQuery<IGroupVulnerabilityDrafts>(GET_GROUP_VULNERABILITY_DRAFTS, {
    fetchPolicy: "cache-first",
    variables: { canRetrieveDrafts, first: 150, groupName, search: "" },
  });

  const refetchAll = useCallback((): void => {
    void refetch();
    void vulnDraftsRefetch();
  }, [refetch, vulnDraftsRefetch]);

  useEffect((): void => {
    async function fetchData(): Promise<void> {
      setVulnData(await getVulnerabilitiesCriteriaData());
      setRequirementData(await getRequerimentsData());
    }

    void fetchData();
  }, [setVulnData, setRequirementData]);

  const vulnerabilities: IVulnRowAttr[] = useMemo((): IVulnRowAttr[] => {
    return data === undefined ? [] : formatVulnerability(data);
  }, [data]);
  const vulnDrafts: IVulnRowAttr[] = useMemo((): IVulnRowAttr[] => {
    return vulnDraftsData === undefined
      ? []
      : formatVulnerabilityDrafts(vulnDraftsData);
  }, [vulnDraftsData]);
  const draftTotal =
    !_.isUndefined(vulnDraftsData) &&
    !_.isUndefined(vulnDraftsData.group.vulnerabilityDrafts) &&
    !_.isUndefined(vulnDraftsData.group.vulnerabilityDrafts.total)
      ? vulnDraftsData.group.vulnerabilityDrafts.total
      : 0;
  const vulnerabilityTotal =
    !_.isUndefined(data) &&
    !_.isUndefined(data.group.vulnerabilities) &&
    !_.isUndefined(data.group.vulnerabilities.total)
      ? data.group.vulnerabilities.total
      : 0;
  const size = draftTotal + vulnerabilityTotal;
  const vulnerabilitiesZeroRisk =
    vulnsZeroRisk === undefined ? [] : formatVulnerability(vulnsZeroRisk);

  const handleNextPage = useCallback(async (): Promise<void> => {
    const pageInfo =
      data === undefined
        ? { endCursor: "", hasNextPage: false }
        : data.group.vulnerabilities.pageInfo;

    if (pageInfo.hasNextPage) {
      await fetchMore({ variables: { after: pageInfo.endCursor } });
    }
    const draftPageInfo =
      !_.isUndefined(vulnDraftsData) &&
      !_.isUndefined(vulnDraftsData.group.vulnerabilityDrafts)
        ? vulnDraftsData.group.vulnerabilityDrafts.pageInfo
        : { endCursor: "", hasNextPage: false };

    if (draftPageInfo.hasNextPage) {
      await vulnDraftsFetchMore({ variables: { after: pageInfo.endCursor } });
    }
  }, [data, fetchMore, vulnDraftsData, vulnDraftsFetchMore]);

  const toggleModal = useCallback((): void => {
    setIsOpen(true);
  }, []);

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

  useEffect((): void => {
    setVulnFilters(
      (currentFilter: IFilter<IVulnRowAttr>[]): IFilter<IVulnRowAttr>[] => {
        return currentFilter.map(
          (filter: IFilter<IVulnRowAttr>): IFilter<IVulnRowAttr> => {
            if (
              filter.id === "verification" &&
              // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition
              (typeof filter.key === "string" || filter.key === undefined)
            ) {
              return filter.value === undefined
                ? filter
                : {
                    ...tableFilters.reduce(
                      (prev, curr): IFilter<IVulnRowAttr> => {
                        return curr.id === "verification" ? curr : prev;
                      },
                      tableFilters[4]
                    ),
                    value: filter.value.toString(),
                  };
            }

            return filter;
          }
        );
      }
    );
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const refetchWithFilters = useDebouncedCallback((filterToSearch): void => {
    void refetch(filterToSearch);
    void vulnDraftsRefetch({
      root: _.get(filterToSearch, "root", undefined),
      search: _.get(filterToSearch, "search", undefined),
      stateStatus: _.get(filterToSearch, "stateStatus", undefined),
      type: _.get(filterToSearch, "type", undefined),
    });
  }, 500);

  useEffect((): (() => void) => {
    const filterToSearch = vulnFilters.reduce(
      (prev, curr): Record<string, string> => {
        const title = formatVulnAttribute(curr.id);

        return {
          ...prev,
          [title]: curr.value,
        };
      },
      {}
    );

    refetchWithFilters(filterToSearch);

    return (): void => {
      refetchWithFilters.cancel();
    };
  }, [vulnFilters, refetch, refetchWithFilters, vulnDraftsRefetch]);

  const handleSearch = useDebouncedCallback((search: string): void => {
    void refetch({ search });
  }, 500);

  const filteredDataset = useFilters(
    vulnerabilities.concat(vulnDrafts),
    vulnFilters
  );

  return (
    <React.StrictMode>
      <React.Fragment>
        <div>
          <VulnComponent
            columnToggle={true}
            columns={tableColumns}
            enableColumnFilters={false}
            extraButtons={
              <ActionButtons
                areRequestedZeroRiskVulns={
                  getRequestedZeroRiskVulns(vulnerabilitiesZeroRisk).length > 0
                }
                areSubmittedVulns={getSubmittedVulns(vulnDrafts).length > 0}
                areVulnsPendingOfAcceptance={false}
                areVulnsSelected={
                  remediationModal.selectedVulnerabilities.length > 0
                }
                isEditing={isEditing}
                isOpen={isOpen}
                isRequestingReattack={isRequestingVerify}
                isVerifying={isVerifying}
                onEdit={toggleEdit}
                onRequestReattack={toggleRequestVerify}
                onVerify={toggleVerify}
                openHandleAcceptance={toggleHandleAcceptanceModal}
                openModal={toggleModal}
              />
            }
            filters={
              <Filters filters={vulnFilters} setFilters={setVulnFilters} />
            }
            id={"groupVulns"}
            isEditing={isEditing}
            isRequestingReattack={isRequestingVerify}
            isVerifyingRequest={isVerifying}
            onNextPage={handleNextPage}
            onSearch={handleSearch}
            onVulnSelect={openRemediationModal}
            refetchData={_.debounce(refetchAll, 1000)}
            requirementData={requirementData}
            size={size}
            vulnData={vulnData}
            vulnerabilities={filteredDataset}
          />
        </div>
        {isOpen && (
          <UpdateVerificationModal
            clearSelected={_.get(remediationModal, "clearSelected")}
            handleCloseModal={closeRemediationModal}
            isReattacking={isRequestingVerify}
            isVerifying={isVerifying}
            refetchData={refetchAll}
            refetchFindingAndGroup={undefined}
            refetchFindingHeader={undefined}
            setRequestState={toggleRequestVerify}
            setVerifyState={toggleVerify}
            vulns={remediationModal.selectedVulnerabilities}
          />
        )}
        {isHandleAcceptanceModalOpen && (
          <HandleAcceptanceModal
            groupName={groupName}
            handleCloseModal={toggleHandleAcceptanceModal}
            refetchData={_.debounce(refetchAll, 1500)}
            vulns={vulnerabilitiesZeroRisk.concat(vulnDrafts)}
          />
        )}
        {isEditing && (
          <Modal
            onClose={handleCloseUpdateModal}
            open={isEditing}
            title={t("searchFindings.tabDescription.editVuln")}
          >
            <UpdateDescription
              groupName={groupName}
              handleClearSelected={_.get(remediationModal, "clearSelected")}
              handleCloseModal={handleCloseUpdateModal}
              refetchData={refetchAll}
              vulnerabilities={remediationModal.selectedVulnerabilities}
            />
          </Modal>
        )}
      </React.Fragment>
    </React.StrictMode>
  );
};

export { GroupVulnerabilitiesView };
