import type { IVulnDataTypeAttr } from "scenes/Dashboard/components/Vulnerabilities/types";

interface IUpdateSeverityProps {
  findingId: string;
  vulnerabilities: IVulnDataTypeAttr[];
  handleCloseModal: () => void;
  refetchData: () => void;
}

export type { IUpdateSeverityProps };
