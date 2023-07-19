import { useMutation } from "@apollo/client";
import { useContext } from "react";
import { useTranslation } from "react-i18next";

import { UPDATE_TOURS } from "./queries";

import type { IAuthContext } from "context/auth";
import { authContext } from "context/auth";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

interface ITour {
  tours: {
    newGroup: boolean;
    newRiskExposure: boolean;
    newRoot: boolean;
    welcome: boolean;
  };
  setCompleted: (tour: keyof ITour["tours"]) => void;
}

const useTour = (): ITour => {
  const { t } = useTranslation();
  const user = useContext(authContext as React.Context<Required<IAuthContext>>);
  // GraphQL operations
  const [updateTours] = useMutation(UPDATE_TOURS, {
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred fetching tours", error);
      });
    },
  });
  const setCompleted = (tour: keyof ITour["tours"]): void => {
    user.setUser({
      ...user,
      tours: {
        ...user.tours,
        [tour]: true,
      },
      userEmail: user.userEmail,
      userIntPhone: user.userIntPhone,
      userName: user.userName,
    });

    void updateTours({
      variables: {
        ...user.tours,
        [tour]: true,
      },
    });
  };

  const { tours } = user;

  return { setCompleted, tours };
};

export { useTour };
