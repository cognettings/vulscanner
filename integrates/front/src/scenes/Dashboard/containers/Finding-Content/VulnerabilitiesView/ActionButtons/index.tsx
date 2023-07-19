import React, { useEffect } from "react";
import { useTranslation } from "react-i18next";

import { CloseVulnerabilitiesButton } from "./CloseVulnerabilitiesButton";
import { EditButton } from "./EditButton";
import { HandleAcceptanceButton } from "./HandleAcceptanceButton";
import { NotifyButton } from "./NotifyButton";
import { ReattackVulnButton } from "./ReattackVulnButton";
import { ResubmitVulnerabilitiesButton } from "./ResubmitVulnerabilitiesButton";
import { UpdateSeverityButton } from "./UpdateSeverityButton";
import { VerifyVulnerabilitiesButton } from "./VerifyVulnerabilitiesButton";

import type { IConfirmFn } from "components/ConfirmDialog";
import { ButtonToolbarRow } from "components/Layout";
import { Have } from "context/authz/Have";
import { msgInfo } from "utils/notifications";

interface IActionButtonsProps {
  areVulnerableLocations?: boolean;
  areVulnsSelected: boolean;
  areVulnsPendingOfAcceptance: boolean;
  areRejectedVulns?: boolean;
  areRequestedZeroRiskVulns: boolean;
  areSubmittedVulns: boolean;
  isClosing?: boolean;
  isEditing: boolean;
  isFindingReleased?: boolean;
  isOpen: boolean;
  isRequestingReattack: boolean;
  isResubmitting?: boolean;
  isVerified?: boolean;
  isVerifying: boolean;
  status?: "SAFE" | "VULNERABLE";
  onClosing?: (confirm: IConfirmFn) => () => void;
  onCancel?: () => void;
  onEdit: () => void;
  onNotify?: () => void;
  onRequestReattack: () => void;
  onResubmit?: () => void;
  onVerify: () => void;
  onUpdateSeverity?: () => void;
  openHandleAcceptance: () => void;
  openModal: () => void;
}

const ActionButtons: React.FC<IActionButtonsProps> = ({
  areVulnerableLocations = false,
  areRejectedVulns = false,
  areVulnsSelected,
  areVulnsPendingOfAcceptance,
  areRequestedZeroRiskVulns,
  areSubmittedVulns,
  isClosing = false,
  isEditing,
  isFindingReleased = true,
  isOpen,
  isRequestingReattack,
  isResubmitting = false,
  isVerified = false,
  isVerifying,
  status = "VULNERABLE",
  onClosing,
  onEdit,
  onNotify,
  onRequestReattack,
  onResubmit,
  onCancel,
  onVerify,
  onUpdateSeverity,
  openHandleAcceptance,
  openModal,
}: Readonly<IActionButtonsProps>): JSX.Element => {
  const { t } = useTranslation();
  const displayMessage: () => void = (): void => {
    msgInfo(
      t("searchFindings.tabVuln.info.text"),
      t("searchFindings.tabVuln.info.title"),
      !isRequestingReattack || isOpen
    );
  };
  useEffect(displayMessage, [isRequestingReattack, isOpen, t]);

  return (
    <ButtonToolbarRow>
      <HandleAcceptanceButton
        areRequestedZeroRiskVulns={areRequestedZeroRiskVulns}
        areSubmittedVulns={areSubmittedVulns}
        areVulnsPendingOfAcceptance={areVulnsPendingOfAcceptance}
        isClosing={isClosing}
        isEditing={isEditing}
        isRequestingReattack={isRequestingReattack}
        isResubmitting={isResubmitting}
        isVerifying={isVerifying}
        openHandleAcceptance={openHandleAcceptance}
      />
      {status === "VULNERABLE" && onNotify && (
        <NotifyButton
          isDisabled={false}
          isFindingReleased={isFindingReleased}
          onNotify={onNotify}
        />
      )}
      <Have I={"can_report_vulnerabilities"}>
        <VerifyVulnerabilitiesButton
          areVulnsSelected={areVulnsSelected}
          isClosing={isClosing}
          isEditing={isEditing}
          isRequestingReattack={isRequestingReattack}
          isResubmitting={isResubmitting}
          isVerified={isVerified}
          isVerifying={isVerifying}
          onVerify={onVerify}
          openModal={openModal}
        />
      </Have>
      <Have I={"can_report_vulnerabilities"}>
        <ResubmitVulnerabilitiesButton
          areRejectedVulns={areRejectedVulns}
          isClosing={isClosing}
          isEditing={isEditing}
          isRequestingReattack={isRequestingReattack}
          isResubmitting={isResubmitting}
          isVerifying={isVerifying}
          onCancel={onCancel}
          onResubmit={onResubmit}
        />
        <CloseVulnerabilitiesButton
          areVulnerableLocations={areVulnerableLocations}
          isClosing={isClosing}
          isEditing={isEditing}
          isRequestingReattack={isRequestingReattack}
          isResubmitting={isResubmitting}
          isVerifying={isVerifying}
          onCancel={onCancel}
          onClosing={onClosing}
        />
      </Have>
      <Have I={"is_continuous"}>
        <Have I={"can_report_vulnerabilities"}>
          <ReattackVulnButton
            areVulnsSelected={areVulnsSelected}
            isClosing={isClosing}
            isEditing={isEditing}
            isFindingReleased={isFindingReleased}
            isRequestingReattack={isRequestingReattack}
            isResubmitting={isResubmitting}
            isVerifying={isVerifying}
            onRequestReattack={onRequestReattack}
            openModal={openModal}
            status={status}
          />
        </Have>
      </Have>
      {onUpdateSeverity && (
        <UpdateSeverityButton
          isDisabled={!areVulnsSelected}
          onUpdateSeverity={onUpdateSeverity}
        />
      )}
      <EditButton
        isClosing={isClosing}
        isDisabled={!areVulnsSelected}
        isEditing={isEditing}
        isFindingReleased={isFindingReleased}
        isRequestingReattack={isRequestingReattack}
        isResubmitting={isResubmitting}
        isVerifying={isVerifying}
        onEdit={onEdit}
      />
    </ButtonToolbarRow>
  );
};

export type { IActionButtonsProps };
export { ActionButtons };
