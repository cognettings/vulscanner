import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";

interface IPermanentlyAcceptedFormProps {
  onCancel: () => void;
  refetchData: () => void;
  vulnerabilities: IVulnRowAttr[];
}

interface IFormValues {
  justification: string;
}

export type { IFormValues, IPermanentlyAcceptedFormProps };
