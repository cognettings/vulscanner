import { rmSync } from "fs";
import { join, sep } from "path";

import { sync } from "glob";
// eslint-disable-next-line import/no-unresolved
import { workspace } from "vscode";

const removeFilesCallback = (paths: string[]): void => {
  paths.forEach((path: string): void => {
    rmSync(path, { force: true, recursive: true });
  });
};

const ignoreFiles = (path: string, patterns: string[]): void => {
  patterns.forEach((pattern: string): void => {
    const matches = sync(join(path, pattern));
    removeFilesCallback(matches);
  });
};

const getGroupsPath = (): string => {
  if (!workspace.workspaceFolders) {
    return "";
  }
  const currentPath = workspace.workspaceFolders[0].uri.path;
  if (!currentPath.includes("groups")) {
    return "";
  }

  return join(currentPath.split("groups")[0], "groups");
};

const getRootInfoFromPath = (
  path: string
): { groupName: string; nickname: string; fileRelativePath: string } | null => {
  const groupsIndex = path
    .split(sep)
    .findIndex((item): boolean => item === "groups");
  if (groupsIndex === -1 || path.split(sep).slice(groupsIndex + 1).length < 2) {
    return null;
  }

  const [groupName, nickname] = path.split(sep).slice(groupsIndex + 1);
  const fileRelativePath = path
    .split(sep)
    .slice(groupsIndex + 3)
    .join(sep);

  return { fileRelativePath, groupName, nickname };
};

export { ignoreFiles, getGroupsPath, getRootInfoFromPath };
