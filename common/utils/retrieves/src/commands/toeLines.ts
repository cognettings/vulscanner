/* eslint-disable fp/no-mutation, fp/no-let */
import { existsSync } from "fs";
import { join } from "path";

import type { MessageHandlerData } from "@estruyf/vscode";
import type { ExtensionContext } from "vscode";
// eslint-disable-next-line import/no-unresolved
import { Uri, ViewColumn, window, workspace } from "vscode";

import { getToeLines } from "@retrieves/api/toeLines";
import type { GitRootTreeItem } from "@retrieves/treeItems/gitRoot";
import type { IToeLines } from "@retrieves/types";
import { getGroupsPath } from "@retrieves/utils/file";
import { getWebviewContent } from "@retrieves/utils/webview";

const toeLines = (context: ExtensionContext, node: GitRootTreeItem): void => {
  const panel = window.createWebviewPanel(
    "toe-lines",
    "Toe Lines",
    ViewColumn.One,
    {
      enableScripts: true,
      retainContextWhenHidden: true,
    }
  );

  panel.webview.onDidReceiveMessage(
    (message: {
      command: string;
      requestId: string;
      payload: { message: string };
    }): void => {
      const { command, requestId, payload } = message;
      switch (command) {
        case "GET_ROUTE": {
          void panel.webview.postMessage({
            command,
            payload: "toeLines",
            // The requestId is used to identify the response
            requestId,
          } as MessageHandlerData<string>);
          break;
        }
        case "GET_DATA_TOE_LINES": {
          void getToeLines(node.groupName, node.rootId).then((toe): void => {
            const nodes = toe.map((edge): IToeLines => {
              const rootPath = join(
                getGroupsPath(),
                node.groupName,
                node.nickname
              );
              const uri = Uri.parse(
                `file://${join(rootPath, edge.node.filename)}`
              );

              return { ...edge.node, fileExists: existsSync(uri.fsPath) };
            });
            void panel.webview.postMessage({
              command,
              payload: nodes,
              // The requestId is used to identify the response
              requestId,
            } as MessageHandlerData<IToeLines[]>);
          });
          break;
        }
        case "GET_ROOT_ID": {
          void panel.webview.postMessage({
            command,
            payload: node.rootId,
            // The requestId is used to identify the response
            requestId,
          } as MessageHandlerData<string>);

          break;
        }
        case "POST_DATA": {
          void window.showInformationMessage(
            `Received data from the webview: ${payload.message}`
          );
          break;
        }
        case "TOE_LINES_OPEN_FILE": {
          const rootPath = join(getGroupsPath(), node.groupName, node.nickname);
          const uri = Uri.parse(
            `file://${join(rootPath, String(payload.message))}`
          );
          void window.showTextDocument(uri);
          break;
        }
        case "GET_ROOT": {
          void panel.webview.postMessage({
            command,
            payload: {
              gitignore: [],
              groupName: node.groupName,
              id: node.rootId,
              nickname: node.nickname,
              state: "ACTIVE",
            },
            // The requestId is used to identify the response
            requestId,
          } as MessageHandlerData<unknown>);
          break;
        }
        case "GET_API_TOKEN": {
          void panel.webview.postMessage({
            command,
            payload:
              workspace.getConfiguration("fluidattacks").get("api_token") ??
              workspace.getConfiguration("fluidattacks").get("apiToken") ??
              process.env.INTEGRATES_API_TOKEN ??
              "",
            // The requestId is used to identify the response
            requestId,
          } as MessageHandlerData<string>);
          break;
        }
        default:
          break;
      }
    },
    undefined,
    context.subscriptions
  );

  // eslint-disable-next-line fp/no-mutation
  panel.webview.html = getWebviewContent(context, panel.webview);
};

export { toeLines };
