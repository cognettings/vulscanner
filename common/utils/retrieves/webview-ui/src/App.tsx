import { ApolloProvider } from "@apollo/client";
import { messageHandler } from "@estruyf/vscode/dist/client";
// eslint-disable-next-line import/no-extraneous-dependencies
import { getClient } from "@retrieves/utils/api";
import { useMemo, useState } from "react";
import { render } from "react-dom";
import { MemoryRouter, Route, Routes } from "react-router-dom";

import { GitEnvironmentUrls } from "@webview/containers/GitEnvironmentUrls";
import { ToeLines } from "@webview/containers/ToeLines";

import "@webview/styles.css";

const App = (): JSX.Element => {
  const [apiToken, setApiToken] = useState<string>("");
  const [route, setRoute] = useState<string>();

  useMemo((): void => {
    void messageHandler.request<string>("GET_ROUTE").then((msg): void => {
      setRoute(msg);
    });
  }, []);

  useMemo((): void => {
    void messageHandler.request<string>("GET_API_TOKEN").then((msg): void => {
      setApiToken(msg);
    });
  }, []);

  if (route === undefined) {
    return <div />;
  }

  return (
    <ApolloProvider client={getClient(apiToken)}>
      <div className={"app"}>
        <MemoryRouter initialEntries={[`/${route}`]}>
          <Routes>
            <Route element={<ToeLines />} path={"toeLines"} />
            <Route
              element={<GitEnvironmentUrls />}
              path={"gitEnvironmentUrls"}
            />
          </Routes>
        </MemoryRouter>
      </div>
    </ApolloProvider>
  );
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars
declare const acquireVsCodeApi: <T = unknown>() => {
  getState: () => T;
  setState: (data: T) => void;
  postMessage: (msg: unknown) => void;
};

const elm = document.querySelector("#root");
if (elm) {
  render(<App />, elm);
}
