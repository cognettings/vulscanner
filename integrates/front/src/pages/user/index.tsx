import React from "react";
import { Redirect, Route, Switch, useRouteMatch } from "react-router-dom";

import { Config } from "./config";

const User: React.FC = (): JSX.Element => {
  const { path } = useRouteMatch();

  return (
    <Switch>
      <Route exact={true} path={`${path}/config`}>
        <Config />
      </Route>
      <Redirect to={"/config"} />
    </Switch>
  );
};

export { User };
