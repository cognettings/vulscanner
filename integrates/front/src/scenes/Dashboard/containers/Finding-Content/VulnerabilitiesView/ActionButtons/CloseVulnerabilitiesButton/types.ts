import type { IConfirmFn } from "components/ConfirmDialog";

export interface ICloseVulnerabilitiesButtonProps {
  areVulnerableLocations: boolean;
  isClosing: boolean;
  isEditing: boolean;
  isRequestingReattack: boolean;
  isResubmitting: boolean;
  isVerifying: boolean;
  onCancel?: () => void;
  onClosing?: (confirm: IConfirmFn) => () => void;
}
