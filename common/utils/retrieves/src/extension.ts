/* eslint-disable fp/no-mutating-methods */
/*
 * The module 'vscode' contains the VS Code extensibility API
 * Import the module and reference it with the alias vscode in your code below
 */
import _ from "lodash";
import { flatten, partial } from "ramda";
import { simpleGit } from "simple-git";
import type { ExtensionContext } from "vscode";
import {
  commands,
  languages,
  window,
  workspace,
  // eslint-disable-next-line import/no-unresolved
} from "vscode";

import { getGroups } from "@retrieves/api/groups";
import { getGroupGitRootsSimple } from "@retrieves/api/root";
import { acceptVulnerabilityTemporary } from "@retrieves/commands/acceptVulnerabilityTemporary";
import { addLineToYaml } from "@retrieves/commands/addLineToYaml";
import { clone } from "@retrieves/commands/clone";
import { environmentUrls } from "@retrieves/commands/environmentUrls";
import { goToCriteria } from "@retrieves/commands/goToCriteria";
import { requestReattack } from "@retrieves/commands/requestReattack";
import { setToken } from "@retrieves/commands/setToken";
import { showExtensionLog } from "@retrieves/commands/showExtensionLog";
import { toeLines } from "@retrieves/commands/toeLines";
import { updateToeLinesAttackedLines } from "@retrieves/commands/updateToeLinesAttackedLines";
import {
  setDiagnosticsToAllFiles,
  subscribeToDocumentChanges,
} from "@retrieves/diagnostics/vulnerabilities";
import { GroupsProvider } from "@retrieves/providers/groups";
import type { IGitRoot } from "@retrieves/types";
import { Logger } from "@retrieves/utils/logging";

const activate = async (context: ExtensionContext): Promise<void> => {
  Logger.info("Initialized the extension");

  await commands.executeCommand("setContext", "fluidattacks.hackerMode", false);
  await commands.executeCommand(
    "setContext",
    "fluidattacks.groupsAvailable",
    false
  );
  await commands.executeCommand(
    "setContext",
    "fluidattacks.identifiedRepository",
    false
  );
  void commands.registerCommand("fluidattacks.setToken", setToken);

  const apiToken: string | undefined =
    process.env.INTEGRATES_API_TOKEN ??
    workspace.getConfiguration("fluidattacks").get("apiToken");
  if (_.isNil(apiToken) || !workspace.workspaceFolders) {
    Logger.error("Undefined API token or no open workspace found");

    return;
  }
  await context.globalState.update("apiKey", apiToken);

  const currentWorkingDir = workspace.workspaceFolders[0].uri.path;
  Logger.info(`Current working directory is ${currentWorkingDir}`);
  const retrievesDiagnostics =
    languages.createDiagnosticCollection("fluidattacks");
  context.subscriptions.push(retrievesDiagnostics);

  void commands.registerCommand("fluidattacks.showOutput", showExtensionLog);

  void commands.registerCommand(
    "fluidattacks.goToCriteria",
    partial(goToCriteria, [retrievesDiagnostics])
  );

  void commands.registerCommand(
    "fluidattacks.requestReattack",
    partial(requestReattack, [retrievesDiagnostics])
  );
  void commands.registerCommand(
    "fluidattacks.acceptVulnerabilityTemporary",
    partial(acceptVulnerabilityTemporary, [retrievesDiagnostics])
  );

  if (currentWorkingDir.includes("groups")) {
    await commands.executeCommand(
      "setContext",
      "fluidattacks.hackerMode",
      true
    );
    Logger.info("Hacker mode enabled");
    void commands.executeCommand(
      "setContext",
      "fluidattacks.groupsAvailable",
      true
    );
    context.subscriptions.push(
      commands.registerCommand(
        "fluidattacks.lines",
        partial(toeLines, [context])
      )
    );

    context.subscriptions.push(
      commands.registerCommand(
        "fluidattacks.environmentUrls",
        partial(environmentUrls, [context])
      )
    );

    void window.registerTreeDataProvider("user_groups", new GroupsProvider());

    void commands.registerCommand("fluidattacks.clone", clone);

    void commands.registerCommand(
      "fluidattacks.updateToeLinesAttackedLines",
      updateToeLinesAttackedLines
    );

    commands.registerCommand("fluidattacks.addSelectedText", addLineToYaml);

    subscribeToDocumentChanges(context, retrievesDiagnostics);
  } else {
    Logger.info("User mode enabled");
    const repo = simpleGit(currentWorkingDir);
    const gitRemote = (await repo.listRemote(["--get-url"])).toString();
    const gitRoot = flatten(
      await Promise.all(
        (
          await getGroups()
        ).map(async (group): Promise<IGitRoot[]> => {
          const result = await getGroupGitRootsSimple(group);

          return result;
        })
      )
    ).find((root): boolean => {
      return (
        root.url === gitRemote ||
        root.nickname === currentWorkingDir.split("/").slice(-1)[0]
      );
    });

    if (gitRoot === undefined) {
      await window.showWarningMessage(
        "Could not identify the repository. Please open the editor on the base directory of the root."
      );

      return;
    }
    await commands.executeCommand(
      "setContext",
      "fluidattacks.identifiedRepository",
      true
    );
    await context.globalState.update("rootNickname", gitRoot.nickname);

    await setDiagnosticsToAllFiles(
      retrievesDiagnostics,
      gitRoot.groupName,
      gitRoot.id,
      gitRoot.nickname,
      currentWorkingDir
    );
  }
};

export { activate };
