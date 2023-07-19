export interface IHandleAcceptanceButtonProps {
  areVulnsPendingOfAcceptance: boolean;
  areRequestedZeroRiskVulns: boolean;
  areSubmittedVulns: boolean;
  isClosing: boolean;
  isEditing: boolean;
  isRequestingReattack: boolean;
  isResubmitting: boolean;
  isVerifying: boolean;
  openHandleAcceptance: () => void;
}
