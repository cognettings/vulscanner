import { useQuery } from "@apollo/client";
import { faCheck } from "@fortawesome/free-solid-svg-icons";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";

import { GET_ME_VULNERABILITIES_ASSIGNED_IDS } from "./queries";
import { TaskIndicator } from "./styles";
import type { IGetMeVulnerabilitiesAssignedIds } from "./types";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { Tooltip } from "components/Tooltip";
import { Logger } from "utils/logger";

const ToDo: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { push } = useHistory();

  const { data } = useQuery<IGetMeVulnerabilitiesAssignedIds>(
    GET_ME_VULNERABILITIES_ASSIGNED_IDS,
    {
      fetchPolicy: "cache-first",
      onError: ({ graphQLErrors }): void => {
        graphQLErrors.forEach((error): void => {
          Logger.error(
            "An error occurred fetching vulnerabilities assigned ids",
            error
          );
        });
      },
    }
  );

  const allAssigned =
    data === undefined ? 0 : data.me.vulnerabilitiesAssigned.length;
  const empty = allAssigned === 0;

  const onClick = useCallback((): void => {
    push("/todos");
  }, [push]);

  const limitFormatter = useCallback((assigned: number): string => {
    const maxLimit = 99;

    return assigned > maxLimit ? `${maxLimit}+` : `${assigned}`;
  }, []);

  return (
    // eslint-disable-next-line react/forbid-component-props
    <Container position={"relative"} style={{ overflowY: "visible" }}>
      <Tooltip
        id={"navbar.task.id"}
        tip={t(`navbar.task.tooltip.${empty ? "assignedless" : "assigned"}`)}
      >
        <Button icon={faCheck} onClick={onClick} size={"md"}>
          {t("components.navBar.toDo")}
        </Button>
      </Tooltip>
      {empty ? undefined : (
        <TaskIndicator>{limitFormatter(allAssigned)}</TaskIndicator>
      )}
    </Container>
  );
};

export { ToDo };
