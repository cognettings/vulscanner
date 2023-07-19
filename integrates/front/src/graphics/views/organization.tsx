import React, { createElement } from "react";
import { render } from "react-dom";
import { BrowserRouter, Route, Switch } from "react-router-dom";

import { ChartsForOrganizationView } from "scenes/Dashboard/containers/Organization-Content/ChartsForOrganizationView";
import { GlobalStyle } from "styles";
import { secureStore, secureStoreContext } from "utils/secureStore";
// eslint-disable-next-line import/no-unresolved
import "vite/modulepreload-polyfill";

const App: React.FC = (): JSX.Element => (
  <React.StrictMode>
    <GlobalStyle />
    <BrowserRouter basename={"/graphics-for-organization"}>
      <secureStoreContext.Provider value={secureStore}>
        <Switch>
          <Route component={ChartsForOrganizationView} path={"/"} />
        </Switch>
      </secureStoreContext.Provider>
    </BrowserRouter>
  </React.StrictMode>
);

render(createElement(App), document.getElementById("root"));
