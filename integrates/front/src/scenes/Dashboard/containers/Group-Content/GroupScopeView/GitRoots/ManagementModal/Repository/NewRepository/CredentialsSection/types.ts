import type { ICredentialsAttr } from "../../../../../types";

interface ICredentialsType {
  credExists: boolean;
  disabledCredsEdit: boolean;
  groupedExistingCreds: Record<string, ICredentialsAttr>;
  isEditing: boolean;
  manyRows: boolean;
  repoUrl: string;
  setCredExists: React.Dispatch<React.SetStateAction<boolean>>;
  setDisabledCredsEdit: React.Dispatch<React.SetStateAction<boolean>>;
  setShowGitAlert: React.Dispatch<React.SetStateAction<boolean>>;
  showGitAlert: boolean;
  validateGitMsg: {
    message: string;
    type: string;
  };
}

export type { ICredentialsType };
