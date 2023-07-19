import type { ISnippet } from "scenes/Dashboard/components/Vulnerabilities/VulnerabilityModal/types";

interface ICodeInfoProps {
  snippet: ISnippet | null;
  specific: string;
}

export type { ICodeInfoProps };
