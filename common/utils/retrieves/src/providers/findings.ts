/* eslint-disable fp/no-this, @typescript-eslint/no-invalid-void-type */
import _ from "lodash";
import type { Event, TreeDataProvider, TreeItem } from "vscode";
import {
  EventEmitter,
  TreeItemCollapsibleState,
  // eslint-disable-next-line import/no-unresolved
} from "vscode";

import { FindingTreeItem } from "@retrieves/treeItems/finding";
import type { VulnerabilityTreeItem } from "@retrieves/treeItems/vulnerability";
import { toVulnerability } from "@retrieves/treeItems/vulnerability";
import type { IFinding, IVulnerability } from "@retrieves/types";

type EventGroup = FindingTreeItem | undefined | void;
type TreeItems = FindingTreeItem[] | VulnerabilityTreeItem[];
// eslint-disable-next-line fp/no-class
class FindingsProvider implements TreeDataProvider<FindingTreeItem> {
  private readonly onDidChangeTreeDataEventEmitter: EventEmitter<EventGroup> =
    new EventEmitter<EventGroup>();

  public constructor(
    private readonly rootPath: string,
    private readonly vulnerabilities: IVulnerability[]
  ) {}

  // eslint-disable-next-line @typescript-eslint/member-ordering
  private readonly vulnerabilitiesByFinding = _.groupBy(
    this.vulnerabilities,
    (vulnerability): string => vulnerability.finding.title
  );

  // eslint-disable-next-line @typescript-eslint/member-ordering
  public readonly onDidChangeTreeData: Event<EventGroup> =
    this.onDidChangeTreeDataEventEmitter.event;

  public refresh(): void {
    this.onDidChangeTreeDataEventEmitter.fire();
  }

  // eslint-disable-next-line class-methods-use-this
  public getTreeItem(element: FindingTreeItem): TreeItem {
    return element;
  }

  public getChildren(element?: FindingTreeItem): TreeItems {
    if (element && element.contextValue === "finding") {
      return this.vulnerabilitiesByFinding[element.label].map(
        (vulnerability): VulnerabilityTreeItem =>
          toVulnerability(this.rootPath, vulnerability)
      );
    } else if (element) {
      return [];
    }

    return this.getFindingItems();
  }

  private getFindingItems(): FindingTreeItem[] {
    const findings = this.vulnerabilities.map(
      (vulnerability): IFinding => vulnerability.finding
    );
    const toFinding = (
      findingTitle: string,
      severityScore: number
    ): FindingTreeItem =>
      new FindingTreeItem(
        findingTitle,
        TreeItemCollapsibleState.Collapsed,
        this.rootPath,
        severityScore
      );

    const finds = _.uniqBy(findings, "title").map(
      (finding): FindingTreeItem =>
        toFinding(finding.title, finding.severityScore)
    );

    return finds;
  }
}

export { FindingsProvider };
