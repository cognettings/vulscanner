import type { ColumnDef } from "@tanstack/react-table";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { changeZeroRiskFormatter } from "./changeZeroRiskFormatter";
import type { IZeroRiskTableProps } from "./types";

import type { IVulnDataAttr } from "../../types";
import { Col, Row } from "components/Layout";
import { MixedCheckBoxButton } from "components/MixedCheckBoxButton";
import { Table } from "components/Table";
import type { ICellHelper } from "components/Table/types";
import { Tooltip } from "components/Tooltip";
import { severityFormatter } from "utils/formatHelpers";

type SwitchOptions = "" | "APPROVED" | "REJECTED";
const ZeroRiskTable: React.FC<IZeroRiskTableProps> = ({
  acceptanceVulns,
  isConfirmRejectZeroRiskSelected,
  setAcceptanceVulns,
}: IZeroRiskTableProps): JSX.Element => {
  const { t } = useTranslation();

  const [isApproved, setIsApproved] = useState<SwitchOptions>("");

  const handleRejectZeroRisk = (vulnInfo?: IVulnDataAttr): void => {
    if (vulnInfo) {
      const newVulnList: IVulnDataAttr[] = acceptanceVulns.map(
        (vuln: IVulnDataAttr): IVulnDataAttr =>
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

  const handleConfirmZeroRisk = (vulnInfo?: IVulnDataAttr): void => {
    if (vulnInfo) {
      const newVulnList: IVulnDataAttr[] = acceptanceVulns.map(
        (vuln: IVulnDataAttr): IVulnDataAttr =>
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

  const columns: ColumnDef<IVulnDataAttr>[] = [
    {
      accessorKey: "where",
      header: "Where",
    },
    {
      accessorKey: "specific",
      header: "Specific",
    },
    {
      accessorKey: "severityTemporalScore",
      cell: (cell: ICellHelper<IVulnDataAttr>): JSX.Element =>
        severityFormatter(cell.getValue()),
      header: "Severity",
    },
    {
      accessorKey: "acceptance",
      cell: (cell: ICellHelper<IVulnDataAttr>): JSX.Element =>
        changeZeroRiskFormatter(
          cell.row.original,
          handleConfirmZeroRisk,
          handleRejectZeroRisk
        ),
      header: "Acceptance",
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
          const newVulnList: IVulnDataAttr[] = acceptanceVulns.map(
            (vuln: IVulnDataAttr): IVulnDataAttr => ({
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
      {isConfirmRejectZeroRiskSelected ? (
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
            id={"vulnsToHandleAcceptance"}
          />
        </React.Fragment>
      ) : undefined}
    </React.StrictMode>
  );
};

export { ZeroRiskTable };
