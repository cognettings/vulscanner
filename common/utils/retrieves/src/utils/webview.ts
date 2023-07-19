import { join } from "path";

import type { ExtensionContext, Webview } from "vscode";
// eslint-disable-next-line import/no-unresolved
import { ExtensionMode, Uri } from "vscode";

const getUri = (
  webview: Webview,
  extensionUri: Uri,
  pathList: string[]
): Uri => {
  return webview.asWebviewUri(Uri.joinPath(extensionUri, ...pathList));
};

const getWebviewContent = (
  context: ExtensionContext,
  webview: Webview
): string => {
  const jsFile = "webview.js";

  const cssUrl = "null";

  const isProduction = context.extensionMode === ExtensionMode.Production;
  const scriptUrl = webview
    .asWebviewUri(Uri.file(join(context.extensionPath, "dist", jsFile)))
    .toString();

  return `<!DOCTYPE html>
      <html lang="en">
      <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          ${isProduction ? `<link href="${cssUrl}" rel="stylesheet">` : ""}
      </head>
      <body>
          <div id="root"></div>

       ${
         isProduction
           ? `<script type="module" src="${scriptUrl}" />`
           : `<script type="module">
                import RefreshRuntime from "http://localhost:9000/@react-refresh"
                RefreshRuntime.injectIntoGlobalHook(window);
                window.$RefreshReg$ = () => {};
                window.$RefreshSig$ = () => (type) => type;
                window.__vite_plugin_react_preamble_installed__ = true;
              </script>
              <script src="http://localhost:9000/@vite/client" type="module"></script>

              <script src="http://localhost:9000/App.tsx" type="module"></script>`
       }
      </body>
      </html>`;
};

export { getUri, getWebviewContent };
