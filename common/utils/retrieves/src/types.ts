/* eslint-disable fp/no-mutation */
import type { DiagnosticSeverity, Range } from "vscode";
// eslint-disable-next-line import/no-unresolved
import { Diagnostic } from "vscode";

interface IAttackedFile {
  success: boolean;
  message?: string;
}

interface IGroup {
  name: string;
  subscription: string;
}

interface IOrganization {
  groups: IGroup[];
}

interface IGitRoot {
  id: string;
  nickname: string;
  groupName: string;
  state: "ACTIVE" | "INACTIVE";
  gitignore: string[];
  downloadUrl?: string;
  url?: string;
  gitEnvironmentUrls: {
    id: string;
    url: string;
  }[];
}

interface IToeLines {
  attackedLines: number;
  bePresent: boolean;
  filename: string;
  comments: string;
  modifiedDate: string;
  loc: number;
  fileExists?: boolean;
  sortsPriorityFactor: number;
}

interface IVulnerability {
  id: string;
  specific: string;
  where: string;
  reportDate: string;
  rootNickname: string;
  state: "REJECTED" | "SAFE" | "SUBMITTED" | "VULNERABLE";
  finding: IFinding;
}

interface IFinding {
  description: string;
  id: string;
  title: string;
  severityScore: number;
}

class VulnerabilityDiagnostic extends Diagnostic {
  public vulnerabilityId?: string;

  public findingId?: string;

  public constructor(
    findingId: string,
    vulnId: string,
    range: Range,
    message: string,
    severity?: DiagnosticSeverity
  ) {
    super(range, message, severity);

    this.vulnerabilityId = vulnId;
    this.findingId = findingId;
  }
}

export type {
  IAttackedFile,
  IFinding,
  IGitRoot,
  IGroup,
  IOrganization,
  IToeLines,
  IVulnerability,
};

export { VulnerabilityDiagnostic };
