import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";

interface ISubmittedFormProps {
  changePermissions?: (groupName: string) => void;
  findingId?: string;
  displayGlobalColumns?: boolean;
  groupName?: string;
  onCancel: () => void;
  refetchData: () => void;
  vulnerabilities: IVulnRowAttr[];
}

interface IFormValues {
  justification?: string;
  rejectionReasons: string[];
  otherRejectionReason?: string;
}

export type { IFormValues, ISubmittedFormProps };
