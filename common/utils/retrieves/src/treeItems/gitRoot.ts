/* eslint-disable @typescript-eslint/parameter-properties */
import type { Command } from "vscode";
// eslint-disable-next-line import/no-unresolved
import { ThemeIcon, TreeItem, TreeItemCollapsibleState } from "vscode";

import { getGroupGitRoots } from "@retrieves/api/root";
import type { IGitRoot } from "@retrieves/types";

class GitRootTreeItem extends TreeItem {
  public contextValue = "gitRoot";

  public readonly iconPath = new ThemeIcon("git-merge");

  public constructor(
    public readonly label: string,
    public readonly collapsibleState: TreeItemCollapsibleState,
    public readonly groupName: string,
    public readonly rootId: string,
    public readonly nickname: string,
    public readonly gitignore: string[],
    public readonly downloadUrl?: string,
    public readonly command?: Command
  ) {
    super(label, collapsibleState);
  }
}

const getGitRoots = async (groupName: string): Promise<GitRootTreeItem[]> => {
  const roots: IGitRoot[] = await getGroupGitRoots(groupName);

  const toGitRoot = (root: IGitRoot): GitRootTreeItem => {
    return new GitRootTreeItem(
      root.nickname,
      TreeItemCollapsibleState.None,
      groupName,
      root.id,
      root.nickname,
      root.gitignore,
      root.downloadUrl
    );
  };

  const deps = roots
    .filter(
      (root: IGitRoot): boolean =>
        root.state === "ACTIVE" && root.downloadUrl !== undefined
    )
    .map((dep): GitRootTreeItem => toGitRoot(dep));

  return deps;
};

export { getGitRoots, GitRootTreeItem };
