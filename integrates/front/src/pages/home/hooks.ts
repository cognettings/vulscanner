import { useQuery } from "@apollo/client";
import Bugsnag from "@bugsnag/js";
import LogRocket from "logrocket";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import { useContext } from "react";

import type { ICurrentUser } from "./queries";
import { GET_CURRENT_USER } from "./queries";

import type { IAuthContext } from "context/auth";
import { authContext } from "context/auth";
import { authzPermissionsContext } from "context/authz/config";
import { Logger } from "utils/logger";
import { initializeDelighted, initializeZendesk } from "utils/widgets";

const useCurrentUser = (): ICurrentUser["me"] | undefined => {
  const user = useContext(authContext as React.Context<Required<IAuthContext>>);
  const permissions = useContext(authzPermissionsContext);

  const { data } = useQuery<ICurrentUser>(GET_CURRENT_USER, {
    fetchPolicy: "cache-first",
    onCompleted: ({ me }): void => {
      user.setUser({
        tours: {
          newGroup: me.tours.newGroup,
          newRiskExposure: me.tours.newRiskExposure,
          newRoot: me.tours.newRoot,
          welcome: me.tours.welcome,
        },
        userEmail: me.userEmail,
        userIntPhone:
          me.phone === null
            ? undefined
            : `+${me.phone.callingCountryCode}${me.phone.nationalNumber}`,
        userName: me.userName,
      });
      permissions.update(
        me.permissions.map((action): { action: string } => ({ action }))
      );
      LogRocket.identify(me.userEmail, {
        email: me.userEmail,
        name: me.userName,
      });
      Bugsnag.setUser(me.userEmail, me.userEmail, me.userName);

      mixpanel.identify(me.userEmail);
      mixpanel.register({
        User: me.userName,
        // Intentional snake case
        // eslint-disable-next-line camelcase
        integrates_user_email: me.userEmail,
      });
      mixpanel.people.set({ $email: me.userEmail, $name: me.userName });

      initializeDelighted(me.userEmail, me.userName);
      initializeZendesk(me.userEmail, me.userName);
    },
    onError: (error): void => {
      error.graphQLErrors.forEach(({ message }): void => {
        Logger.error("Couldn't load current user", message);
      });
    },
  });

  if (data === undefined) {
    return undefined;
  }

  return data.me;
};

export { useCurrentUser };
