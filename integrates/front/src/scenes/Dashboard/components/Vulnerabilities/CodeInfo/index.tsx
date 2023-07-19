import { faList } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import { highlightAll } from "prismjs";
import React, { useEffect } from "react";
import { useTranslation } from "react-i18next";

import type { ICodeInfoProps } from "./types";

import "prismjs/themes/prism-coy.css";
import "prismjs/plugins/line-highlight/prism-line-highlight.js";
import "prismjs/plugins/line-highlight/prism-line-highlight.css";

const CodeInfo: React.FC<ICodeInfoProps> = ({
  snippet,
  specific,
}: ICodeInfoProps): JSX.Element => {
  const { t } = useTranslation();
  useEffect((): void => {
    highlightAll();
  }, []);

  return (
    <div className={"Code"} data-private={true}>
      <pre
        className={"line-highlight"}
        data-line={String(Number(specific))}
        data-line-offset={_.isNil(snippet) ? 0 : snippet.offset}
      >
        {_.isNil(snippet) || _.isEmpty(snippet.content) ? (
          <div className={"no-data"}>
            <FontAwesomeIcon icon={faList} size={"3x"} />
            <p>{t("searchFindings.tabVuln.contentTab.code.noData")}</p>
          </div>
        ) : (
          <code className={"language-none"}>{snippet.content}</code>
        )}
      </pre>
    </div>
  );
};

export { CodeInfo };
