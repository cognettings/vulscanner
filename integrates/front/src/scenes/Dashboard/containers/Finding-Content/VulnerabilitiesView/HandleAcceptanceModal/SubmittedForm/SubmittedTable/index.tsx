import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type { ColumnDef, Row as TableRow } from "@tanstack/react-table";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import type { FormEvent } from "react";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { changeSubmittedFormatter } from "./changeSubmittedFormatter";
import type { ISubmittedTableProps } from "./types";

import { Col, Row } from "components/Layout";
import { MixedCheckBoxButton } from "components/MixedCheckBoxButton";
import { Table } from "components/Table";
import type { ICellHelper } from "components/Table/types";
import { Tooltip } from "components/Tooltip";
import { authzPermissionsContext } from "context/authz/config";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { VulnerabilityModal } from "scenes/Dashboard/components/Vulnerabilities/VulnerabilityModal";
import { severityFormatter } from "utils/formatHelpers";

type SwitchOptions = "" | "APPROVED" | "REJECTED";
const SubmittedTable: React.FC<ISubmittedTableProps> = (
  props: ISubmittedTableProps
): JSX.Element => {
  const {
    acceptanceVulns,
    changePermissions,
    displayGlobalColumns = false,
    isConfirmRejectVulnerabilitySelected,
    setAcceptanceVulns,
    refetchData,
  } = props;
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

  const { t } = useTranslation();
  const [isApproved, setIsApproved] = useState<SwitchOptions>("");
  const [currentRow, setCurrentRow] = useState<IVulnRowAttr>();

  const openAdditionalInfoModal = useCallback(
    (rowInfo: TableRow<IVulnRowAttr>): ((event: FormEvent) => void) => {
      return (event: FormEvent): void => {
        if (changePermissions !== undefined) {
          changePermissions(rowInfo.original.groupName);
        }
        setCurrentRow(rowInfo.original);
        mixpanel.track("ViewDraftVulnerability", {
          groupName: rowInfo.original.groupName,
        });
        event.stopPropagation();
      };
    },
    [changePermissions]
  );
  const closeAdditionalInfoModal: () => void = useCallback((): void => {
    setCurrentRow(undefined);
  }, []);

  const handleRejectSubmitted = (vulnInfo?: IVulnRowAttr): void => {
    if (vulnInfo) {
      const newVulnList: IVulnRowAttr[] = acceptanceVulns.map(
        (vuln: IVulnRowAttr): IVulnRowAttr =>
          vuln.id === vulnInfo.id
            ? {
                ...vuln,
                acceptance: vuln.acceptance === "REJECTED" ? "" : "REJECTED",
              }
            : vuln
      );
      setAcceptanceVulns([...newVulnList]);
    }
  };

  const handleConfirmSubmitted = (vulnInfo?: IVulnRowAttr): void => {
    if (vulnInfo) {
      const newVulnList: IVulnRowAttr[] = acceptanceVulns.map(
        (vuln: IVulnRowAttr): IVulnRowAttr =>
          vuln.id === vulnInfo.id
            ? {
                ...vuln,
                acceptance: vuln.acceptance === "APPROVED" ? "" : "APPROVED",
              }
            : vuln
      );
      setAcceptanceVulns([...newVulnList]);
    }
  };

  const columns: ColumnDef<IVulnRowAttr>[] = [
    ...(displayGlobalColumns
      ? ([
          {
            accessorKey: "groupName",
            header: t(
              "searchFindings.tabVuln.handleAcceptanceModal.submittedForm.submittedTable.groupName"
            ),
          },
          {
            accessorFn: (row): string | undefined => row.finding?.title,
            accessorKey: "finding",
            header: t(
              "searchFindings.tabVuln.handleAcceptanceModal.submittedForm.submittedTable.type"
            ),
          },
        ] as ColumnDef<IVulnRowAttr>[])
      : []),
    {
      accessorKey: "where",
      header: t(
        "searchFindings.tabVuln.handleAcceptanceModal.submittedForm.submittedTable.where"
      ),
    },
    {
      accessorKey: "specific",
      header: t(
        "searchFindings.tabVuln.handleAcceptanceModal.submittedForm.submittedTable.specific"
      ),
    },
    {
      accessorKey: "severityTemporalScore",
      cell: (cell: ICellHelper<IVulnRowAttr>): JSX.Element =>
        severityFormatter(cell.getValue()),
      header: t(
        "searchFindings.tabVuln.handleAcceptanceModal.submittedForm.submittedTable.severity"
      ),
    },
    {
      accessorKey: "acceptance",
      cell: (cell: ICellHelper<IVulnRowAttr>): JSX.Element =>
        changeSubmittedFormatter(
          cell.row.original,
          handleConfirmSubmitted,
          handleRejectSubmitted
        ),
      header: t(
        "searchFindings.tabVuln.handleAcceptanceModal.submittedForm.submittedTable.acceptance"
      ),
    },
  ];

  const getUpdatedValue = useCallback(
    (
      currentValue: SwitchOptions,
      newValue: "APPROVED" | "REJECTED"
    ): SwitchOptions => {
      if (newValue === "APPROVED") {
        return currentValue === "APPROVED" ? "" : "APPROVED";
      }

      return currentValue === "REJECTED" ? "" : "REJECTED";
    },
    []
  );

  const handleOnChange = useCallback(
    (newValue: "APPROVED" | "REJECTED"): (() => void) => {
      return (): void => {
        setIsApproved((currentValue: SwitchOptions): SwitchOptions => {
          const newVulnList: IVulnRowAttr[] = acceptanceVulns.map(
            (vuln: IVulnRowAttr): IVulnRowAttr => ({
              ...vuln,
              acceptance: getUpdatedValue(currentValue, newValue),
            })
          );
          setAcceptanceVulns([...newVulnList]);

          return getUpdatedValue(currentValue, newValue);
        });
      };
    },
    [acceptanceVulns, getUpdatedValue, setAcceptanceVulns]
  );

  return (
    <React.StrictMode>
      {isConfirmRejectVulnerabilitySelected ? (
        <React.Fragment>
          <Row align={"center"} justify={"end"}>
            <Col lg={45} />
            <Col lg={20} md={20}>
              <Tooltip
                id={"toogleToolTip"}
                place={"top"}
                tip={t(
                  "searchFindings.tabDescription.handleAcceptanceModal.zeroRisk.globalSwitch.tooltip"
                )}
              >
                <span className={"mb0 mt1 pr2"}>
                  {t(
                    "searchFindings.tabDescription.handleAcceptanceModal.zeroRisk.globalSwitch.text"
                  )}
                </span>
              </Tooltip>
            </Col>
            <Col lg={35} md={35}>
              <div className={"ma0 pa0 pointer"}>
                <MixedCheckBoxButton
                  fontSize={"fs-checkbox"}
                  id={"zeroRiskCheckBox"}
                  isNoEnabled={isApproved !== "APPROVED"}
                  isSelected={isApproved !== ""}
                  isYesEnabled={isApproved !== "REJECTED"}
                  noLabel={isApproved === "REJECTED" ? "REJECTED" : "REJECT"}
                  onApprove={handleOnChange("APPROVED")}
                  onDelete={handleOnChange("REJECTED")}
                  yesLabel={isApproved === "APPROVED" ? "CONFIRMED" : "CONFIRM"}
                />
              </div>
            </Col>
          </Row>
          <Table
            columns={columns}
            data={acceptanceVulns}
            id={"submittedTable"}
            onRowClick={openAdditionalInfoModal}
          />
          {currentRow ? (
            <VulnerabilityModal
              canDisplayHacker={canRetrieveHacker}
              canRemoveVulnsTags={canRemoveVulnsTags}
              canRequestZeroRiskVuln={canRequestZeroRiskVuln}
              canSeeSource={canSeeSource}
              canUpdateVulnsTreatment={canUpdateVulnsTreatment}
              clearSelectedVulns={undefined}
              closeModal={closeAdditionalInfoModal}
              currentRow={currentRow}
              findingId={currentRow.findingId}
              groupName={currentRow.groupName}
              isFindingReleased={false}
              isModalOpen={true}
              refetchData={refetchData}
            />
          ) : undefined}
        </React.Fragment>
      ) : undefined}
    </React.StrictMode>
  );
};

export { SubmittedTable };
