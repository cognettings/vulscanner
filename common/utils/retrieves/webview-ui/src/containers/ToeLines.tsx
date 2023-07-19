/* eslint-disable react-hooks/rules-of-hooks */
import { messageHandler } from "@estruyf/vscode/dist/client";
import type { IGitRoot, IToeLines } from "@retrieves/types";
import {
  VSCodeButton,
  VSCodeDataGrid,
  VSCodeDataGridCell,
  VSCodeDataGridRow,
} from "@vscode/webview-ui-toolkit/react";
import { useCallback, useMemo, useState } from "react";

import { ToeLinesRow } from "@webview/components/ToeLinesRow";
// eslint-disable-next-line import/no-extraneous-dependencies, import/no-namespace

import "@webview/styles.css";

const ToeLines = (): JSX.Element => {
  const [toeLines, setToeLines] = useState<IToeLines[]>();
  const [root, setRoot] = useState<IGitRoot>();
  const [hideAttackedFiles, setHideAttackedFiles] = useState<boolean>(false);
  const [hideNoLongerPresent, setHideNoLongerPresent] =
    useState<boolean>(false);
  useMemo((): void => {
    if (!toeLines) {
      void messageHandler
        .request<IToeLines[]>("GET_DATA_TOE_LINES")
        .then((msg): void => {
          setToeLines(msg);
        });
    }
  }, [toeLines]);
  useMemo((): void => {
    void messageHandler.request<IGitRoot>("GET_ROOT").then((msg): void => {
      setRoot(msg);
    });
  }, []);

  return (
    <div>
      <VSCodeButton
        onClick={useCallback((): void => {
          setHideAttackedFiles(!hideAttackedFiles);
        }, [hideAttackedFiles])}
      >
        {hideAttackedFiles ? "Show attacked files" : "Hide attacked files"}
      </VSCodeButton>
      <VSCodeButton
        onClick={useCallback((): void => {
          setHideNoLongerPresent(!hideNoLongerPresent);
        }, [hideNoLongerPresent])}
      >
        {hideNoLongerPresent
          ? "Show non-present files"
          : "Hide non-present files"}
      </VSCodeButton>
      <VSCodeDataGrid>
        <VSCodeDataGridRow>
          {[
            "Filename",
            "Attacked",
            "Attacked lines",
            "LOC",
            "Modified",
            "Comment",
            "Sorts Priority Factor",
          ].map((row, index): JSX.Element => {
            return (
              <VSCodeDataGridCell gridColumn={String(index + 1)} key={row}>
                {row}
              </VSCodeDataGridCell>
            );
          })}
        </VSCodeDataGridRow>

        {(toeLines ?? [])
          .filter((item): boolean => {
            if (hideAttackedFiles && item.attackedLines >= item.loc) {
              return false;
            }
            if (hideNoLongerPresent && !item.bePresent) {
              return false;
            }

            return Boolean(root);
          })
          .map((item): JSX.Element => {
            return (
              <ToeLinesRow
                groupName={root?.groupName ?? ""}
                key={item.filename}
                node={item}
                rootId={root?.id ?? ""}
              />
            );
          })}
      </VSCodeDataGrid>
    </div>
  );
};

export { ToeLines };
