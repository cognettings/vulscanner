import { useLazyQuery } from "@apollo/client";
import _ from "lodash";
import { useCallback } from "react";
import { useTranslation } from "react-i18next";

import type { IStakeholder } from "./queries";
import { GET_STAKEHOLDER } from "./queries";

import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

interface IStakeholderAutofill {
  autofill: IStakeholder | Record<string, never>;
  loadAutofill: (event: React.FocusEvent<HTMLInputElement>) => void;
}

const useStakeholderAutofill = (
  type: "group" | "organization" | "user",
  groupName: string | undefined,
  organizationId: string | undefined
): IStakeholderAutofill => {
  const { t } = useTranslation();
  const [getUser, { data }] = useLazyQuery<IStakeholder>(GET_STAKEHOLDER, {
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        if (error.message !== "Access denied or stakeholder not found") {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.error("Couldn't get stakeholder autofill", error);
        }
      });
    },
  });

  const loadAutofill = useCallback(
    (event: React.FocusEvent<HTMLInputElement>): void => {
      const userEmail = event.target.value;

      if (type !== "user" && !_.isEmpty(userEmail)) {
        void getUser({
          variables: {
            entity: type === "organization" ? "ORGANIZATION" : "GROUP",
            groupName: groupName ?? "-",
            organizationId: organizationId ?? "-",
            userEmail,
          },
        });
      }
    },
    [getUser, groupName, organizationId, type]
  );

  const autofill = data === undefined ? {} : data.stakeholder;

  return { autofill, loadAutofill };
};

export { useStakeholderAutofill };
