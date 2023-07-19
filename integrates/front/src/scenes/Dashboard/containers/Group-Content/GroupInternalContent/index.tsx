import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import React, { useContext } from "react";
import { Redirect, Route, Switch, useRouteMatch } from "react-router-dom";

import { ToeContent } from "../ToeContent";
import { authzPermissionsContext } from "context/authz/config";
import { groupContext } from "scenes/Dashboard/group/context";
import type { IGroupContext } from "scenes/Dashboard/group/types";

const GroupInternalContent: React.FC = (): JSX.Element => {
  const { path } = useRouteMatch<{ path: string; url: string }>();
  const { path: groupPath }: IGroupContext = useContext(groupContext);
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canSeeInternalToe: boolean = permissions.can("see_internal_toe");

  return (
    <React.StrictMode>
      <Switch>
        {canSeeInternalToe ? (
          <Route path={`${path}/surface`}>
            <ToeContent isInternal={true} />
          </Route>
        ) : undefined}
        <Redirect to={groupPath} />
      </Switch>
    </React.StrictMode>
  );
};

export { GroupInternalContent };
