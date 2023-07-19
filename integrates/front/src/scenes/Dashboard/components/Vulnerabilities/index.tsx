import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type {
  ColumnDef,
  Row,
  SortingState,
  VisibilityState,
} from "@tanstack/react-table";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, {
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import type { FormEvent } from "react";
import { useTranslation } from "react-i18next";
import { useHistory, useParams, useRouteMatch } from "react-router-dom";

import {
  handleDeleteVulnerabilityHelper,
  onRemoveVulnResultHelper,
} from "./helpers";
import { VulnerabilityModal } from "./VulnerabilityModal";

import type { IRemoveVulnAttr } from "../RemoveVulnerability/types";
import { Table } from "components/Table";
import { deleteFormatter } from "components/Table/formatters/deleteFormatter";
import type { ICellHelper } from "components/Table/types";
import {
  authzGroupContext,
  authzPermissionsContext,
} from "context/authz/config";
import { useStoredState } from "hooks/use-stored-state";
import { DeleteVulnerabilityModal } from "scenes/Dashboard/components/RemoveVulnerability/index";
import type {
  IVulnComponentProps,
  IVulnRowAttr,
} from "scenes/Dashboard/components/Vulnerabilities/types";
import {
  filterOutVulnerabilities,
  formatVulnerabilities,
  getNonSelectableVulnerabilitiesOnCloseIds,
  getNonSelectableVulnerabilitiesOnReattackIds,
  getNonSelectableVulnerabilitiesOnResubmitIds,
  getNonSelectableVulnerabilitiesOnVerifyIds,
} from "scenes/Dashboard/components/Vulnerabilities/utils";

function usePreviousProps(value: boolean): boolean {
  const ref = useRef(false);
  useEffect((): void => {
    // eslint-disable-next-line fp/no-mutation
    ref.current = value;
  });

  return ref.current;
}

export const VulnComponent: React.FC<IVulnComponentProps> = ({
  changePermissions,
  columnFilterSetter = undefined,
  columnFilterState = undefined,
  columnToggle = false,
  columns,
  columnDefaultVisibility = {},
  csvColumns,
  csvHeaders,
  enableColumnFilters = true,
  exportCsv = false,
  extraButtons = undefined,
  filters = undefined,
  findingState = "VULNERABLE",
  hasNextPage,
  id,
  isClosing = false,
  isEditing,
  isFindingReleased = true,
  isRequestingReattack,
  isResubmitting = false,
  isVerifyingRequest,
  isUpdatingSeverity = false,
  refetchData,
  size = undefined,
  nonValidOnReattackVulnerabilities,
  vulnerabilities,
  onNextPage = undefined,
  onSearch = undefined,
  onVulnSelect = (): void => undefined,
  vulnData = undefined,
  requirementData = undefined,
}: IVulnComponentProps): JSX.Element => {
  const { vulnerabilityId: vulnId } = useParams<{
    vulnerabilityId: string | undefined;
  }>();
  const { url } = useRouteMatch<{ url: string }>();
  const history = useHistory();
  const { t } = useTranslation();
  const attributes: PureAbility<string> = useContext(authzGroupContext);
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canRemoveVulnsTags: boolean = permissions.can(
    "api_mutations_remove_vulnerability_tags_mutate"
  );
  const canRequestZeroRiskVuln: boolean = permissions.can(
    "api_mutations_request_vulnerabilities_zero_risk_mutate"
  );
  const canSeeSource: boolean = permissions.can("see_vulnerability_source");
  const canUpdateVulnsTreatment: boolean = permissions.can(
    "api_mutations_update_vulnerabilities_treatment_mutate"
  );
  const canRetrieveHacker: boolean = permissions.can(
    "api_resolvers_vulnerability_hacker_resolve"
  );
  const canResubmitVulnerabilities: boolean = permissions.can(
    "api_mutations_resubmit_vulnerabilities_mutate"
  );
  const canRemoveVulns: boolean =
    permissions.can("api_mutations_remove_vulnerability_mutate") &&
    attributes.can("can_report_vulnerabilities");
  const [columnVisibility, setColumnVisibility] =
    useStoredState<VisibilityState>(
      `${id}-visibilityState`,
      columnDefaultVisibility
    );
  const [sorting, setSorting] = useStoredState<SortingState>(
    `${id}-sortingState`,
    []
  );
  const [selectedVulnerabilities, setSelectedVulnerabilities] = useState<
    IVulnRowAttr[]
  >([]);
  const [vulnerabilityId, setVulnerabilityId] = useState(vulnId ?? "");
  const [vulnToDeleteId, setVulnToDeleteId] = useState("");
  const [isDeleteVulnOpen, setIsDeleteVulnOpen] = useState(false);
  const [isVulnerabilityModalOpen, setIsVulnerabilityModalOpen] =
    useState(false);
  const [currentRow, setCurrentRow] = useState<IVulnRowAttr>();
  const previousIsEditing = usePreviousProps(isEditing);
  const previousIsRequestingReattack = usePreviousProps(isRequestingReattack);
  const previousIsClosing = usePreviousProps(isClosing);
  const previousIsResubmitting = usePreviousProps(isResubmitting);
  const previousIsVerifyingRequest = usePreviousProps(isVerifyingRequest);
  const previousIsUpdatingSeverity = usePreviousProps(isUpdatingSeverity);

  const openAdditionalInfoModal = useCallback(
    (rowInfo: Row<IVulnRowAttr>): ((event: FormEvent) => void) => {
      return (event: FormEvent): void => {
        if (changePermissions !== undefined) {
          changePermissions(rowInfo.original.groupName);
        }
        history.replace(`${url}/${rowInfo.original.id}`);
        setVulnerabilityId(rowInfo.original.id);
        setCurrentRow(rowInfo.original);
        mixpanel.track("ViewVulnerability", {
          groupName: rowInfo.original.groupName,
        });
        setIsVulnerabilityModalOpen(true);
        event.stopPropagation();
      };
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [url, changePermissions]
  );
  const closeAdditionalInfoModal: () => void = useCallback((): void => {
    const lastRoutePosition = url.lastIndexOf("/");
    history.replace(`${url.substring(0, lastRoutePosition)}`);
    setVulnerabilityId("");
    setIsVulnerabilityModalOpen(false);
  }, [history, url]);
  const handleCloseDeleteModal: () => void = useCallback((): void => {
    setIsDeleteVulnOpen(false);
  }, []);
  const onDeleteVulnResult = useCallback(
    (removeVulnResult: IRemoveVulnAttr): void => {
      refetchData();
      onRemoveVulnResultHelper(removeVulnResult, t);
      setIsDeleteVulnOpen(false);
    },
    [refetchData, t]
  );
  const handleDeleteVulnerability = useCallback(
    (vulnInfo: IVulnRowAttr | undefined): void => {
      handleDeleteVulnerabilityHelper(
        vulnInfo as unknown as Record<string, string>,
        setVulnToDeleteId,
        setIsDeleteVulnOpen,
        setCurrentRow,
        vulnerabilities
      );
    },
    [vulnerabilities]
  );
  const clearSelectedVulns: () => void = useCallback((): void => {
    setSelectedVulnerabilities([]);
  }, []);

  function onVulnSelection(): void {
    if (previousIsRequestingReattack && !isRequestingReattack) {
      setSelectedVulnerabilities([]);
      onVulnSelect([], clearSelectedVulns);
    }
    if (previousIsVerifyingRequest && !isVerifyingRequest) {
      setSelectedVulnerabilities([]);
      onVulnSelect([], clearSelectedVulns);
    }
    if (previousIsEditing && !isEditing) {
      setSelectedVulnerabilities([]);
      onVulnSelect([], clearSelectedVulns);
    }
    if (previousIsUpdatingSeverity && !isUpdatingSeverity) {
      setSelectedVulnerabilities([]);
      onVulnSelect([], clearSelectedVulns);
    }
    if (!previousIsRequestingReattack && isRequestingReattack) {
      setSelectedVulnerabilities(
        (currentVulnerabilities: IVulnRowAttr[]): IVulnRowAttr[] => {
          const nonValidIds =
            nonValidOnReattackVulnerabilities === undefined
              ? []
              : nonValidOnReattackVulnerabilities.map(
                  (vulnerability: IVulnRowAttr): string => vulnerability.id
                );
          const newVulnerabilities: IVulnRowAttr[] = filterOutVulnerabilities(
            currentVulnerabilities,
            vulnerabilities,
            getNonSelectableVulnerabilitiesOnReattackIds
          ).filter(
            (vuln: IVulnRowAttr): boolean => !nonValidIds.includes(vuln.id)
          );

          onVulnSelect(newVulnerabilities, clearSelectedVulns);

          return newVulnerabilities;
        }
      );
    }
    if (!previousIsResubmitting && isResubmitting) {
      setSelectedVulnerabilities(
        (currentVulnerabilities: IVulnRowAttr[]): IVulnRowAttr[] => {
          const newVulnerabilities: IVulnRowAttr[] = filterOutVulnerabilities(
            currentVulnerabilities,
            vulnerabilities,
            getNonSelectableVulnerabilitiesOnResubmitIds
          );

          onVulnSelect(newVulnerabilities, clearSelectedVulns);

          return newVulnerabilities;
        }
      );
    }
    if (!previousIsClosing && isClosing) {
      setSelectedVulnerabilities(
        (currentVulnerabilities: IVulnRowAttr[]): IVulnRowAttr[] => {
          const newVulnerabilities: IVulnRowAttr[] = filterOutVulnerabilities(
            currentVulnerabilities,
            vulnerabilities,
            getNonSelectableVulnerabilitiesOnCloseIds
          );

          onVulnSelect(newVulnerabilities, clearSelectedVulns);

          return newVulnerabilities;
        }
      );
    }
    if (!previousIsVerifyingRequest && isVerifyingRequest) {
      setSelectedVulnerabilities(
        (currentVulnerabilities: IVulnRowAttr[]): IVulnRowAttr[] => {
          const newVulnerabilities: IVulnRowAttr[] = filterOutVulnerabilities(
            currentVulnerabilities,
            vulnerabilities,
            getNonSelectableVulnerabilitiesOnVerifyIds
          );

          onVulnSelect(newVulnerabilities, clearSelectedVulns);

          return newVulnerabilities;
        }
      );
    }
    onVulnSelect(selectedVulnerabilities, clearSelectedVulns);
  }
  // Annotation needed as adding the dependencies creates a memory leak
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(onVulnSelection, [
    selectedVulnerabilities,
    onVulnSelect,
    isClosing,
    isEditing,
    isRequestingReattack,
    isResubmitting,
    isVerifyingRequest,
    isUpdatingSeverity,
    previousIsClosing,
    previousIsEditing,
    previousIsRequestingReattack,
    previousIsResubmitting,
    previousIsVerifyingRequest,
    previousIsUpdatingSeverity,
  ]);

  const enabledRows = useCallback(
    (row: Row<IVulnRowAttr>): boolean => {
      if (
        (isVerifyingRequest || isRequestingReattack) &&
        (row.original.state === "REJECTED" ||
          row.original.state === "SAFE" ||
          row.original.state === "SUBMITTED")
      ) {
        return false;
      }
      if (
        isRequestingReattack &&
        (row.original.verification?.toLowerCase() === "requested" ||
          row.original.verification?.toLowerCase() === "on_hold")
      ) {
        return false;
      }
      if (
        isVerifyingRequest &&
        row.original.verification?.toLowerCase() !== "requested"
      ) {
        return false;
      }
      if (isResubmitting && row.original.state !== "REJECTED") {
        return false;
      }
      if (isClosing && row.original.state !== "VULNERABLE") {
        return false;
      }

      return true;
    },
    [isClosing, isRequestingReattack, isResubmitting, isVerifyingRequest]
  );

  const findingId: string = useMemo(
    (): string => (currentRow === undefined ? "" : currentRow.findingId),
    [currentRow]
  );
  const groupName: string = useMemo(
    (): string => (currentRow === undefined ? "" : currentRow.groupName),
    [currentRow]
  );

  const deleteAction = useCallback(
    (cell: ICellHelper<IVulnRowAttr>): JSX.Element => {
      if (cell.row.original.state === "SAFE") {
        return <span />;
      }

      return deleteFormatter(cell.row.original, handleDeleteVulnerability);
    },
    [handleDeleteVulnerability]
  );

  const deleteColumn: ColumnDef<IVulnRowAttr>[] = [
    {
      accessorKey: "id",
      cell: deleteAction,
      enableColumnFilter: false,
      header: t("searchFindings.tabDescription.action"),
    },
  ];

  const orderedVulns: IVulnRowAttr[] = _.orderBy(
    formatVulnerabilities({
      requirementsData: requirementData,
      vulnerabilities,
      vulnsData: vulnData,
    }),
    ["state", "severityTemporalScore"],
    ["desc", "desc"]
  );

  useEffect((): void => {
    if (vulnerabilityId !== "" && orderedVulns.length > 0) {
      const rowInfo: IVulnRowAttr | undefined = orderedVulns.find(
        (item): boolean => item.id === vulnerabilityId
      );
      if (_.isUndefined(rowInfo)) {
        const lastRoutePosition = url.lastIndexOf("/");
        history.replace(`${url.substring(0, lastRoutePosition)}`);
      } else {
        if (!_.isUndefined(changePermissions)) {
          changePermissions(rowInfo.groupName);
        }
        setCurrentRow(rowInfo);
        mixpanel.track("ViewVulnerability", {
          groupName: rowInfo.groupName,
        });
        setIsVulnerabilityModalOpen(true);
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [vulnerabilityId, orderedVulns.length]);

  return (
    <React.StrictMode>
      <Table
        columnFilterSetter={columnFilterSetter}
        columnFilterState={columnFilterState}
        columnToggle={columnToggle}
        columnVisibilitySetter={setColumnVisibility}
        columnVisibilityState={columnVisibility}
        columns={[...columns, ...(canRemoveVulns ? deleteColumn : [])]}
        csvColumns={csvColumns}
        csvHeaders={csvHeaders}
        data={orderedVulns}
        enableColumnFilters={enableColumnFilters}
        enableRowSelection={enabledRows}
        exportCsv={exportCsv}
        extraButtons={
          extraButtons ? (
            <div className={"dib nr0 nr1-l nr1-m pt1"}>{extraButtons}</div>
          ) : undefined
        }
        filters={filters}
        hasNextPage={hasNextPage}
        id={"vulnerabilitiesTable"}
        onNextPage={onNextPage}
        onRowClick={openAdditionalInfoModal}
        onSearch={onSearch}
        rowSelectionSetter={
          (isFindingReleased && findingState !== "SAFE") ||
          canResubmitVulnerabilities
            ? setSelectedVulnerabilities
            : undefined
        }
        rowSelectionState={selectedVulnerabilities}
        size={size}
        sortingSetter={setSorting}
        sortingState={sorting}
      />
      <DeleteVulnerabilityModal
        findingId={findingId}
        id={vulnToDeleteId}
        onClose={handleCloseDeleteModal}
        onRemoveVulnRes={onDeleteVulnResult}
        open={isDeleteVulnOpen}
      />
      {vulnerabilityId !== "" && currentRow && (
        <VulnerabilityModal
          canDisplayHacker={canRetrieveHacker}
          canRemoveVulnsTags={canRemoveVulnsTags}
          canRequestZeroRiskVuln={canRequestZeroRiskVuln}
          canSeeSource={canSeeSource}
          canUpdateVulnsTreatment={canUpdateVulnsTreatment}
          clearSelectedVulns={clearSelectedVulns}
          closeModal={closeAdditionalInfoModal}
          currentRow={currentRow}
          findingId={findingId}
          groupName={groupName}
          isFindingReleased={isFindingReleased}
          isModalOpen={isVulnerabilityModalOpen}
          refetchData={refetchData}
        />
      )}
    </React.StrictMode>
  );
};
