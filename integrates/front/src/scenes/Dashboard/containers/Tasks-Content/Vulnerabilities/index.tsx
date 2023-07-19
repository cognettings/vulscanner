import { useQuery } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { faSyncAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type {
  ColumnDef,
  ColumnFilter,
  ColumnFiltersState,
} from "@tanstack/react-table";
import _ from "lodash";
import React, {
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import type { IFilter } from "components/Filter";
import { Filters, useFilters } from "components/Filter";
import { ButtonToolbarRow } from "components/Layout";
import { Modal } from "components/Modal";
import { formatLinkHandler } from "components/Table/formatters/linkFormatter";
import {
  authzGroupContext,
  authzPermissionsContext,
} from "context/authz/config";
import { useStoredState, useTabTracking } from "hooks";
import { UpdateVerificationModal } from "scenes/Dashboard/components/UpdateVerificationModal";
import { VulnComponent } from "scenes/Dashboard/components/Vulnerabilities";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { UpdateDescription } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription";
import { formatVulnerabilitiesTreatment } from "scenes/Dashboard/components/Vulnerabilities/utils";
import { EditButton } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/ActionButtons/EditButton";
import type { IModalConfig } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/types";
import { filterVerification } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/utils";
import { ReattackVulnerabilities } from "scenes/Dashboard/containers/Tasks-Content/Vulnerabilities/ActionsButtons/ReattackVulnerabilities/index";
import { GET_ME_VULNERABILITIES_ASSIGNED } from "scenes/Dashboard/containers/Tasks-Content/Vulnerabilities/queries";
import type {
  IAction,
  IGetMeVulnerabilitiesAssigned,
  IGroupAction,
} from "scenes/Dashboard/containers/Tasks-Content/Vulnerabilities/types";
import {
  filteredContinuousVulnerabilitiesOnReattackIds,
  getUserGroups,
} from "scenes/Dashboard/containers/Tasks-Content/Vulnerabilities/utils";
import { GET_USER_ORGANIZATIONS_GROUPS } from "scenes/Dashboard/queries";
import type {
  IGetUserOrganizationsGroups,
  IOrganizationGroups,
} from "scenes/Dashboard/types";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

export const TasksVulnerabilities: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  const [isEditing, setIsEditing] = useState(false);
  const [iscurrentOpen, setIscurrentOpen] = useState<boolean[]>([]);
  const [isReattacking, setIsReattacking] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const attributesContext: PureAbility<string> = useContext(authzGroupContext);
  const permissionsContext: PureAbility<string> = useContext(
    authzPermissionsContext
  );

  const [vulnFilters, setVulnFilters] = useStoredState<ColumnFiltersState>(
    "vulnerabilitiesTable-columnFilters",
    [],
    localStorage
  );
  const [columnFilters, setColumnFilters] = useStoredState<ColumnFiltersState>(
    "tblTodoVulns-columnFilters",
    [],
    localStorage
  );

  const { data: userData } = useQuery<IGetUserOrganizationsGroups>(
    GET_USER_ORGANIZATIONS_GROUPS,
    {
      fetchPolicy: "cache-first",
      onError: ({ graphQLErrors }): void => {
        graphQLErrors.forEach((error): void => {
          Logger.warning("An error occurred fetching user groups", error);
        });
      },
    }
  );
  const {
    data: meVulnerabilitiesAssigned,
    refetch: refetchVulnerabilitiesAssigned,
  } = useQuery<IGetMeVulnerabilitiesAssigned>(GET_ME_VULNERABILITIES_ASSIGNED, {
    fetchPolicy: "cache-first",
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        Logger.warning(
          "An error occurred fetching vulnerabilities assigned from dashboard",
          error
        );
      });
    },
  });

  useTabTracking("Todos");

  const groups = useMemo(
    (): IOrganizationGroups["groups"] => getUserGroups(userData),
    [userData]
  );

  const vulnerabilities: IVulnRowAttr[] = useMemo(
    (): IVulnRowAttr[] =>
      formatVulnerabilitiesTreatment({
        organizationsGroups:
          userData === undefined ? [] : userData.me.organizations,
        vulnerabilities:
          meVulnerabilitiesAssigned === undefined || userData === undefined
            ? []
            : meVulnerabilitiesAssigned.me.vulnerabilitiesAssigned,
      }),
    [meVulnerabilitiesAssigned, userData]
  );

  const vulnerabilitiesGroupName: string[] = useMemo(
    (): string[] =>
      Array.from(
        new Set(
          vulnerabilities.map((vulnerability: IVulnRowAttr): string =>
            vulnerability.groupName.toLowerCase()
          )
        )
      ),
    [vulnerabilities]
  );

  const changePermissions = useCallback(
    (groupName: string): void => {
      permissionsContext.update([]);
      if (userData !== undefined) {
        const recordPermissions: IGroupAction[] = _.flatten(
          userData.me.organizations.map(
            (organization: IOrganizationGroups): IGroupAction[] =>
              organization.groups.map(
                (group: IOrganizationGroups["groups"][0]): IGroupAction => ({
                  actions: group.permissions.map(
                    (action: string): IAction => ({
                      action,
                    })
                  ),
                  groupName: group.name,
                })
              )
          )
        );
        const filteredPermissions: IGroupAction[] = recordPermissions.filter(
          (recordPermission: IGroupAction): boolean =>
            recordPermission.groupName.toLowerCase() === groupName.toLowerCase()
        );
        if (filteredPermissions.length > 0) {
          permissionsContext.update(filteredPermissions[0].actions);
        }
      }
    },
    [permissionsContext, userData]
  );

  const onGroupChange: () => void = (): void => {
    attributesContext.update([]);
    permissionsContext.update([]);
    if (userData !== undefined) {
      const currentPermissions: IAction[][] = _.flatten(
        userData.me.organizations.map(
          (organization: IOrganizationGroups): IAction[][] =>
            organization.groups.map(
              (group: IOrganizationGroups["groups"][0]): IAction[] =>
                group.permissions.map(
                  (action: string): IAction => ({
                    action,
                  })
                )
            )
        )
      );
      const groupsServicesAttributes: IOrganizationGroups["groups"] =
        userData.me.organizations.reduce(
          (
            previousValue: IOrganizationGroups["groups"],
            currentValue
          ): IOrganizationGroups["groups"] => [
            ...previousValue,
            ...currentValue.groups.filter((group): boolean =>
              vulnerabilitiesGroupName.includes(group.name.toLowerCase())
            ),
          ],
          []
        );
      const currentAttributes: string[] = Array.from(
        new Set(
          groupsServicesAttributes.reduce(
            (previous: string[], current): string[] => [
              ...previous,
              ...current.serviceAttributes,
            ],
            []
          )
        )
      );
      if (currentAttributes.length > 0) {
        attributesContext.update(
          currentAttributes.map((action: string): IAction => ({ action }))
        );
      }
      if (currentPermissions.length > 0 && currentPermissions[0].length > 0) {
        permissionsContext.update(
          Array.from(
            new Set(
              currentPermissions.reduce(
                (
                  selectedPermission: IAction[],
                  currentPermission: IAction[]
                ): IAction[] =>
                  currentPermission.length < selectedPermission.length
                    ? currentPermission
                    : selectedPermission,
                currentPermissions[0]
              )
            )
          )
        );
      }
    }
  };

  useEffect(onGroupChange, [
    attributesContext,
    permissionsContext,
    userData,
    vulnerabilitiesGroupName,
  ]);

  const [modalConfig, setModalConfig] = useState<IModalConfig>({
    clearSelected: (): void => undefined,
    selectedVulnerabilities: [],
  });

  const openRemediationModal: (
    vuls: IVulnRowAttr[],
    clearSelected: () => void
  ) => void = useCallback(
    (vulns: IVulnRowAttr[], clearSelected: () => void): void => {
      setModalConfig({
        clearSelected,
        selectedVulnerabilities: vulns,
      });
    },
    []
  );

  const refreshAssigned: () => void = useCallback(async (): Promise<void> => {
    await refetchVulnerabilitiesAssigned();
  }, [refetchVulnerabilitiesAssigned]);

  const columns: ColumnDef<IVulnRowAttr>[] = [
    {
      accessorKey: "organizationName",
      cell: (cell): JSX.Element => {
        const orgName =
          cell.row.original.organizationName === undefined
            ? ""
            : cell.row.original.organizationName;
        const link = `../orgs/${orgName}/groups/${cell.row.original.groupName}`;
        const text = cell.getValue<string>();

        return formatLinkHandler(link, text);
      },
      header: "Organization",
      meta: { filterType: "select" },
    },
    {
      accessorKey: "groupName",
      cell: (cell): JSX.Element => {
        const orgName =
          cell.row.original.organizationName === undefined
            ? ""
            : cell.row.original.organizationName;
        const link = `../orgs/${orgName}/groups/${cell.row.original.groupName}`;
        const text = cell.getValue<string>();

        return formatLinkHandler(link, text);
      },
      header: t("organization.tabs.groups.newGroup.name"),
      meta: { filterType: "select" },
    },
    {
      accessorFn: (row): string | undefined => row.finding?.title,
      cell: (cell): JSX.Element => {
        const orgName =
          cell.row.original.organizationName === undefined
            ? ""
            : cell.row.original.organizationName;
        const findingId =
          cell.row.original.finding === undefined
            ? ""
            : cell.row.original.finding.id;
        const link =
          `../orgs/${orgName}/groups/${cell.row.original.groupName}` +
          `/vulns/${findingId}/locations`;
        const text = cell.getValue<string>();

        return formatLinkHandler(link, text);
      },
      header: t("searchFindings.tabVuln.vulnTable.vulnerabilityType.title"),
      id: "finding-title",
      meta: { filterType: "select" },
    },
    {
      accessorKey: "where",
      enableColumnFilter: false,
      header: t("searchFindings.tabVuln.vulnTable.vulnerability"),
    },
    {
      accessorFn: (): string => "View",
      cell: (cell): JSX.Element => {
        const orgName =
          cell.row.original.organizationName === undefined
            ? ""
            : cell.row.original.organizationName;
        const findingId =
          cell.row.original.finding === undefined
            ? ""
            : cell.row.original.finding.id;
        const link =
          `../orgs/${orgName}/groups/${cell.row.original.groupName}` +
          `/vulns/${findingId}/evidence`;
        const text = cell.getValue<string>();

        return formatLinkHandler(link, text);
      },
      enableColumnFilter: false,
      header: "Evidence",
    },
    {
      accessorFn: (row): string =>
        row.verification === null ? "-" : row.verification,
      header: t("searchFindings.tabVuln.vulnTable.verification"),
      id: "verification",
      meta: { filterType: "select" },
    },
    {
      accessorFn: (row): number => row.severityTemporalScore,
      header: t("searchFindings.tabDescription.severity"),
      id: "severity",
      meta: { filterType: "select" },
    },
    {
      accessorKey: "tag",
      header: t("searchFindings.tabVuln.vulnTable.tags"),
    },
  ];

  const [filters, setFilters] = useState<IFilter<IVulnRowAttr>[]>([
    {
      id: "organizationName",
      key: "organizationName",
      label: "Organization",
      selectOptions: (vulns: IVulnRowAttr[]): string[] =>
        [
          ...new Set(vulns.map((vuln): string => vuln.organizationName ?? "")),
        ].filter(Boolean),
      type: "select",
    },
    {
      id: "groupName",
      key: "groupName",
      label: t("organization.tabs.groups.newGroup.name"),
      type: "text",
    },
    {
      id: "finding-title",
      key: (row, value): boolean => {
        if (_.isEmpty(value)) return true;
        if (_.isEmpty(row.finding?.title)) return false;

        // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
        return row.finding!.title.includes(value!);
      },
      label: t("searchFindings.tabVuln.vulnTable.vulnerabilityType.title"),
      type: "text",
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
      id: "severity",
      key: "severity",
      label: t("searchFindings.tabDescription.severity"),
      type: "numberRange",
    },
    {
      id: "tag",
      key: "tag",
      label: t("searchFindings.tabVuln.vulnTable.tags"),
      type: "text",
    },
  ]);

  useEffect((): void => {
    if (
      columnFilters.filter(
        (element: ColumnFilter): boolean => element.id === "verification"
      ).length > 0
    ) {
      const filtervalue = columnFilters.filter(
        (element: ColumnFilter): boolean => element.id === "verification"
      )[0].value;
      if (
        vulnFilters.filter(
          (element: ColumnFilter): boolean => element.id === "verification"
        ).length > 0
      ) {
        setVulnFilters(
          vulnFilters.map((element: ColumnFilter): ColumnFilter => {
            if (element.id === "verification") {
              return { id: "verification", value: filtervalue };
            }

            return element;
          })
        );
      } else {
        setVulnFilters([
          ...vulnFilters,
          { id: "verification", value: filtervalue },
        ]);
      }
    } else {
      setVulnFilters(
        vulnFilters
          .map((element: ColumnFilter): ColumnFilter => {
            if (element.id === "verification") {
              return { id: "", value: "" };
            }

            return element;
          })
          .filter((element: ColumnFilter): boolean => element.id !== "")
      );
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [columnFilters]);

  const toggleEdit = useCallback((): void => {
    setIscurrentOpen(
      Object.entries(
        _.groupBy(
          modalConfig.selectedVulnerabilities,
          (vuln: IVulnRowAttr): string => vuln.groupName
        )
      ).map((__, index: number): boolean => index === 0)
    );
    setIsEditing(!isEditing);
  }, [isEditing, modalConfig.selectedVulnerabilities]);

  const handleCloseUpdateModal = useCallback(
    (index: number): void => {
      setIscurrentOpen((current: boolean[]): boolean[] => {
        const newCurrent = current.map(
          (isCurrentOpen: boolean, currentIndex: number): boolean => {
            if (currentIndex === index || currentIndex === index + 1) {
              return !isCurrentOpen;
            }

            return isCurrentOpen;
          }
        );
        if (
          newCurrent.every((isCurrentOpen: boolean): boolean => !isCurrentOpen)
        ) {
          setIsEditing(false);
          modalConfig.clearSelected();
        }

        return newCurrent;
      });
    },
    [modalConfig]
  );

  const toggleModal = useCallback((): void => {
    setIsOpen(true);
  }, []);
  const closeRemediationModal = useCallback((): void => {
    setIsOpen(false);
  }, []);
  const onReattack = useCallback((): void => {
    if (isReattacking) {
      setIsReattacking(!isReattacking);
    } else {
      const { selectedVulnerabilities } = modalConfig;
      const validVulnerabilitiesId: string[] =
        filteredContinuousVulnerabilitiesOnReattackIds(
          selectedVulnerabilities,
          groups
        );
      const newValidVulnerabilities: IVulnRowAttr[] = Array.from(
        new Set(
          selectedVulnerabilities.filter(
            (selectedVulnerability: IVulnRowAttr): boolean =>
              validVulnerabilitiesId.includes(selectedVulnerability.id)
          )
        )
      );
      if (selectedVulnerabilities.length > newValidVulnerabilities.length) {
        setIsReattacking(!isReattacking);
        if (newValidVulnerabilities.length === 0) {
          msgError(t("searchFindings.tabVuln.errors.selectedVulnerabilities"));
        } else {
          setModalConfig(
            (currentConfig): IModalConfig => ({
              clearSelected: currentConfig.clearSelected,
              selectedVulnerabilities: newValidVulnerabilities,
            })
          );
          setIsOpen(true);
        }
      } else if (selectedVulnerabilities.length > 0) {
        setIsOpen(true);
        setIsReattacking(!isReattacking);
      } else {
        setIsReattacking(!isReattacking);
      }
    }
  }, [groups, isReattacking, modalConfig, t]);

  const onClose = useCallback(
    (index: number): (() => void) =>
      (): void => {
        handleCloseUpdateModal(index);
      },
    [handleCloseUpdateModal]
  );

  const filteredData = useFilters(vulnerabilities, filters);

  if (_.isUndefined(userData) || _.isEmpty(userData)) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <div>
        <div>
          <VulnComponent
            changePermissions={changePermissions}
            columnFilterSetter={setColumnFilters}
            columnFilterState={columnFilters}
            columns={columns}
            enableColumnFilters={false}
            extraButtons={
              <ButtonToolbarRow>
                <Button
                  disabled={isEditing || isReattacking}
                  id={"refresh-assigned"}
                  onClick={refreshAssigned}
                  variant={"secondary"}
                >
                  <FontAwesomeIcon icon={faSyncAlt} />
                </Button>
                <ReattackVulnerabilities
                  areVulnerabilitiesReattacked={
                    vulnerabilities.filter(
                      (vuln): boolean =>
                        !vuln.remediated &&
                        filteredContinuousVulnerabilitiesOnReattackIds(
                          vulnerabilities,
                          groups
                        ).includes(vuln.id)
                    ).length === 0
                  }
                  areVulnsSelected={
                    modalConfig.selectedVulnerabilities.length > 0
                  }
                  isEditing={isEditing}
                  isOpen={isOpen}
                  isRequestingReattack={isReattacking}
                  onRequestReattack={onReattack}
                  openModal={toggleModal}
                />
                <EditButton
                  isClosing={false}
                  isDisabled={modalConfig.selectedVulnerabilities.length === 0}
                  isEditing={isEditing}
                  isFindingReleased={true}
                  isRequestingReattack={isReattacking}
                  isResubmitting={false}
                  isVerifying={false}
                  onEdit={toggleEdit}
                />
              </ButtonToolbarRow>
            }
            filters={
              <Filters
                dataset={vulnerabilities}
                filters={filters}
                setFilters={setFilters}
              />
            }
            findingState={"VULNERABLE"}
            id={"taskView"}
            isEditing={false}
            isFindingReleased={true}
            isRequestingReattack={isReattacking}
            isVerifyingRequest={false}
            nonValidOnReattackVulnerabilities={Array.from(
              new Set(
                vulnerabilities.filter(
                  (vulnerability: IVulnRowAttr): boolean =>
                    !filteredContinuousVulnerabilitiesOnReattackIds(
                      vulnerabilities,
                      groups
                    ).includes(vulnerability.id)
                )
              )
            )}
            onVulnSelect={openRemediationModal}
            refetchData={refetchVulnerabilitiesAssigned}
            vulnerabilities={filteredData}
          />
        </div>
      </div>
      {isOpen ? (
        <UpdateVerificationModal
          clearSelected={_.get(modalConfig, "clearSelected")}
          handleCloseModal={closeRemediationModal}
          isReattacking={isReattacking}
          isVerifying={false}
          refetchData={refetchVulnerabilitiesAssigned}
          refetchFindingAndGroup={undefined}
          refetchFindingHeader={undefined}
          setRequestState={onReattack}
          setVerifyState={onReattack}
          vulns={modalConfig.selectedVulnerabilities}
        />
      ) : undefined}
      {isEditing && modalConfig.selectedVulnerabilities.length > 0
        ? Object.entries(
            _.groupBy(
              modalConfig.selectedVulnerabilities,
              (vuln: IVulnRowAttr): string => vuln.groupName
            )
          ).map(
            (
              [vulnGroupName, vulnerabilitiesToUpdated]: [
                string,
                IVulnRowAttr[]
              ],
              index: number
            ): JSX.Element => {
              return (
                <Modal
                  key={vulnGroupName}
                  onClose={onClose(index)}
                  open={iscurrentOpen[index]}
                  title={t("searchFindings.tabDescription.editVuln")}
                >
                  <UpdateDescription
                    changePermissions={changePermissions}
                    findingId={""}
                    groupName={vulnGroupName}
                    handleClearSelected={_.get(modalConfig, "clearSelected")}
                    handleCloseModal={onClose(index)}
                    isOpen={iscurrentOpen[index]}
                    refetchData={refetchVulnerabilitiesAssigned}
                    vulnerabilities={vulnerabilitiesToUpdated}
                  />
                </Modal>
              );
            }
          )
        : undefined}
    </React.StrictMode>
  );
};
