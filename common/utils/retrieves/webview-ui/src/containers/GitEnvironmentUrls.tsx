/* eslint-disable react-hooks/rules-of-hooks */
import { messageHandler } from "@estruyf/vscode/dist/client";
import type { IGitRoot } from "@retrieves/types";
import {
  VSCodeDataGrid,
  VSCodeDataGridCell,
  VSCodeDataGridRow,
} from "@vscode/webview-ui-toolkit/react";
import { useMemo, useState } from "react";
// eslint-disable-next-line import/no-extraneous-dependencies, import/no-namespace

import "@webview/styles.css";

const GitEnvironmentUrls = (): JSX.Element => {
  const [root, setRoot] = useState<IGitRoot>();
  const [rootId, setRootId] = useState<string>();

  useMemo((): void => {
    void messageHandler.request<string>("GET_ROOT_ID").then((msg): void => {
      setRootId(msg);
    });
  }, []);

  useMemo((): void => {
    if (rootId !== undefined) {
      void messageHandler
        .request<IGitRoot>("GET_ROOT", { rootId })
        .then((msg): void => {
          setRoot(msg);
        });
    }
  }, [rootId]);
  if (root === undefined) {
    return <div />;
  }

  return (
    <div>
      <VSCodeDataGrid>
        <VSCodeDataGridRow>
          {["url"].map((row, index): JSX.Element => {
            return (
              <VSCodeDataGridCell gridColumn={String(index + 1)} key={row}>
                {row}
              </VSCodeDataGridCell>
            );
          })}
        </VSCodeDataGridRow>

        {root.gitEnvironmentUrls.map((item, index): JSX.Element => {
          return (
            <VSCodeDataGridRow key={item.id}>
              <VSCodeDataGridCell gridColumn={String(index + 1)} />
              {item.url}
            </VSCodeDataGridRow>
          );
        })}
      </VSCodeDataGrid>
    </div>
  );
};

export { GitEnvironmentUrls };
