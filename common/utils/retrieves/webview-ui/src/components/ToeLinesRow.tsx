import { messageHandler } from "@estruyf/vscode/dist/client";
import type { IToeLines } from "@retrieves/types";
import {
  VSCodeDataGridCell,
  VSCodeDataGridRow,
  VSCodeLink,
} from "@vscode/webview-ui-toolkit/react";
import React, { useCallback } from "react";

interface IToeLinesRowProps {
  groupName: string;
  node: IToeLines;
  rootId: string;
}

const ToeLinesRow: React.FC<IToeLinesRowProps> = ({
  node,
  rootId,
  groupName,
}: IToeLinesRowProps): JSX.Element => {
  const {
    filename,
    attackedLines,
    loc,
    modifiedDate,
    comments,
    fileExists,
    sortsPriorityFactor,
  } = node;
  const useOpenFile = useCallback(
    // eslint-disable-next-line @typescript-eslint/explicit-function-return-type
    (name: string) => (): void => {
      messageHandler.send("TOE_LINES_OPEN_FILE", { message: name });
    },
    []
  );

  return (
    <VSCodeDataGridRow key={filename}>
      {[
        filename,
        String(attackedLines >= loc),
        attackedLines,
        loc,
        modifiedDate,
        comments,
        `${sortsPriorityFactor}%`,
      ].map((cell, index): JSX.Element => {
        const context = {
          comments,
          filename,
          groupName,
          rootId,
          webviewSection: "filename",
        };

        return (
          <VSCodeDataGridCell
            data-vscode-context={JSON.stringify(context)}
            gridColumn={String(index + 1)}
            key={undefined}
          >
            {index === 0 && (fileExists ?? false) ? (
              <VSCodeLink
                href={String(cell)}
                // eslint-disable-next-line line-comment-position, no-inline-comments, react-hooks/rules-of-hooks
                onClick={useOpenFile(String(cell))} // NOSONAR
              >
                {cell}
              </VSCodeLink>
            ) : (
              cell
            )}
          </VSCodeDataGridCell>
        );
      })}
    </VSCodeDataGridRow>
  );
};

export { ToeLinesRow };
