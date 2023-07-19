import { useQuery } from "@apollo/client";
import { useCallback, useContext, useState } from "react";
import { openPopupWidget } from "react-calendly";
import { useRouteMatch } from "react-router-dom";

import { GET_GROUP_SERVICES } from "./queries";

import { authContext } from "context/auth";
import { Logger } from "utils/logger";

interface IGetGroupServices {
  group: {
    name: string;
    serviceAttributes: string[];
  };
}

interface IMatchProps {
  orgName: string;
  groupName: string;
}

const useCalendly = (): {
  closeUpgradeModal: () => void;
  isAvailable: boolean;
  isSquadActive: boolean;
  isUpgradeOpen: boolean;
  openCalendly: () => void;
  openUpgradeModal: () => void;
} => {
  const routeMatch = useRouteMatch<IMatchProps>(
    "/orgs/:orgName/groups/:groupName"
  );
  const groupName = routeMatch === null ? "" : routeMatch.params.groupName;

  const { userEmail, userName } = useContext(authContext);
  const [isUpgradeOpen, setIsUpgradeOpen] = useState(false);

  const { data } = useQuery<IGetGroupServices>(GET_GROUP_SERVICES, {
    fetchPolicy: "cache-first",
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        Logger.error("An error occurred fetching group services", error);
      });
    },
    skip: routeMatch === null,
    variables: { groupName },
  });

  const isAvailable = routeMatch !== null && data !== undefined;

  const isSquadActive =
    isAvailable &&
    data.group.serviceAttributes.includes("has_squad") &&
    data.group.serviceAttributes.includes("is_continuous");

  const openUpgradeModal = useCallback((): void => {
    setIsUpgradeOpen(true);
  }, []);

  const closeUpgradeModal = useCallback((): void => {
    setIsUpgradeOpen(false);
  }, []);

  const openCalendly = useCallback((): void => {
    if (isSquadActive) {
      openPopupWidget({
        prefill: {
          customAnswers: { a1: groupName },
          email: userEmail,
          name: userName,
        },
        url: "https://calendly.com/fluidattacks/talk-to-a-hacker",
      });
    }
  }, [isSquadActive, groupName, userEmail, userName]);

  return {
    closeUpgradeModal,
    isAvailable,
    isSquadActive,
    isUpgradeOpen,
    openCalendly,
    openUpgradeModal,
  };
};

export { useCalendly };
