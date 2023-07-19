import "@fontsource/roboto";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useMemo, useState } from "react";
import { render } from "react-dom";
import { BrowserRouter, Route, Switch } from "react-router-dom";

import { GlobalStyle } from "./styles";

import { ToastBox } from "components/Alert";
import type { IAuthContext } from "context/auth";
import { authContext } from "context/auth";
import {
  authzPermissionsContext,
  userLevelPermissions,
} from "context/authz/config";
import type { IFeaturePreviewContext } from "context/featurePreview";
import { featurePreviewContext } from "context/featurePreview";
import type { IMeetingModeContext } from "context/meetingMode";
import { meetingModeContext } from "context/meetingMode";
import { useStoredState } from "hooks";
import { Home } from "pages/home";
import { Login } from "pages/login";
import { SignUp } from "pages/sign-up";
import { ApolloProvider } from "utils/apollo";
import { BugsnagErrorBoundary } from "utils/bugsnagErrorBoundary";
import { getEnvironment } from "utils/environment";
import { initializeLogRocket } from "utils/logRocket";
import { secureStore, secureStoreContext } from "utils/secureStore";
// eslint-disable-next-line import/no-unresolved
import "vite/modulepreload-polyfill";
import "react-toastify/dist/ReactToastify.min.css";
import "tachyons/css/tachyons.min.css";
import "tachyons-word-break/css/tachyons-word-break.min.css";

const App: React.FC = (): JSX.Element => {
  // eslint-disable-next-line fp/no-mutation
  window.global = window;

  const [user, setUser] = useState({
    tours: {
      newGroup: true,
      newRiskExposure: true,
      newRoot: true,
      welcome: true,
    },
    userEmail: "",
    userName: "",
  });
  const [featurePreview, setFeaturePreview] = useStoredState(
    "featurePreview",
    false,
    localStorage
  );
  const [meetingMode, setMeetingMode] = useStoredState(
    "meetingMode",
    false,
    localStorage
  );

  const valueAuth = useMemo((): IAuthContext => ({ ...user, setUser }), [user]);

  const valueFeature = useMemo(
    (): IFeaturePreviewContext => ({ featurePreview, setFeaturePreview }),
    [featurePreview, setFeaturePreview]
  );

  const valueMeetingMode = useMemo(
    (): IMeetingModeContext => ({ meetingMode, setMeetingMode }),
    [meetingMode, setMeetingMode]
  );

  return (
    <React.StrictMode>
      <GlobalStyle />
      <BugsnagErrorBoundary>
        <BrowserRouter basename={"/"}>
          <ApolloProvider>
            <authzPermissionsContext.Provider value={userLevelPermissions}>
              <secureStoreContext.Provider value={secureStore}>
                <authContext.Provider value={valueAuth}>
                  <featurePreviewContext.Provider value={valueFeature}>
                    <meetingModeContext.Provider value={valueMeetingMode}>
                      <Switch>
                        <Route component={Login} exact={true} path={"/"} />
                        <Route component={SignUp} path={"/SignUp"} />
                        <Route component={Home} path={"/"} />
                      </Switch>
                    </meetingModeContext.Provider>
                  </featurePreviewContext.Provider>
                </authContext.Provider>
              </secureStoreContext.Provider>
            </authzPermissionsContext.Provider>
          </ApolloProvider>
        </BrowserRouter>
        <ToastBox autoClose={5000} position={"top-right"} />
      </BugsnagErrorBoundary>
    </React.StrictMode>
  );
};

mixpanel.init("7a7ceb75ff1eed29f976310933d1cc3e");

const environment = getEnvironment();

if (environment === "production") {
  initializeLogRocket();
}

if (environment !== "production") {
  mixpanel.disable();
}

render(<App />, document.getElementById("root"));
