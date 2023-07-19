/* eslint-disable @typescript-eslint/parameter-properties */
import _ from "lodash";
import type { Command, TreeItemCollapsibleState } from "vscode";
// eslint-disable-next-line import/no-unresolved
import { ThemeIcon, TreeItem, Uri } from "vscode";

import { mapScoreToCategory } from "@retrieves/utils/severityScore";

class FindingTreeItem extends TreeItem {
  public contextValue = "finding";

  public readonly iconPath: ThemeIcon | Uri = _.isNil(this.severityScore)
    ? ThemeIcon.Folder
    : Uri.joinPath(
        Uri.parse(__filename),
        "..",
        "..",
        "media",
        `finding_${mapScoreToCategory(this.severityScore)}.svg`
      );

  public constructor(
    public readonly label: string,
    public readonly collapsibleState: TreeItemCollapsibleState,
    public readonly rootPath: string,
    public readonly severityScore?: number,
    public readonly command?: Command
  ) {
    super(label, collapsibleState);
  }
}

export { FindingTreeItem };
