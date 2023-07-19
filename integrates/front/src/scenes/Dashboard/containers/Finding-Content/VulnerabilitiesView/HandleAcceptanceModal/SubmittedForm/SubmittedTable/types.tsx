import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";

interface ISubmittedTableProps {
  acceptanceVulns: IVulnRowAttr[];
  changePermissions?: (groupName: string) => void;
  isConfirmRejectVulnerabilitySelected: boolean;
  displayGlobalColumns?: boolean;
  setAcceptanceVulns: (vulns: IVulnRowAttr[]) => void;
  refetchData: () => void;
}

export type { ISubmittedTableProps };
