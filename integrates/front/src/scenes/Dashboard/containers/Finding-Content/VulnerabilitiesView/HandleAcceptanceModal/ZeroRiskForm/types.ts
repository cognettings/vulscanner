import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";

interface IZeroRiskFormProps {
  groupName: string;
  findingId?: string;
  onCancel: () => void;
  refetchData: () => void;
  vulnerabilities: IVulnRowAttr[];
}

interface IFormValues {
  justification: string;
}

export type { IFormValues, IZeroRiskFormProps };
