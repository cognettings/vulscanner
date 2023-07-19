import type { ApolloError } from "@apollo/client";
// eslint-disable-next-line import/no-unresolved
import { window, workspace } from "vscode";

import { getClient } from "./api";

const armToken: string =
  process.env.INTEGRATES_API_TOKEN ??
  workspace.getConfiguration("fluidattacks").get("apiToken") ??
  "";

const API_CLIENT = getClient(armToken);

const handleGraphQlError = async (apiError: ApolloError): Promise<void> => {
  switch (apiError.message) {
    case "Login required":
      if (armToken) {
        await window.showErrorMessage(
          "This token has no permissions in this repo. Please retry with a valid API token"
        );
      } else {
        await window.showWarningMessage("No token has been set yet");
      }
      break;
    case "Exception - User token has expired":
      await window.showErrorMessage(
        "This token has expired. Please retry with a valid API token"
      );
      break;
    case "Token format unrecognized":
      await window.showErrorMessage(
        "Token format unrecognized. Please retry with a valid API token"
      );
      break;
    default:
      if (apiError.message.includes("Access denied")) {
        await window.showErrorMessage(
          "This token has no permissions in this repo. Please retry with a valid API token"
        );
      } else if (
        apiError.message.includes("request") &&
        apiError.message.includes("failed")
      ) {
        await window.showErrorMessage(
          "Our platform's API endpoint is currently unavailable. Please retry in a few minutes"
        );
        // eslint-disable-next-line no-negated-condition
      } else if (!apiError.message.includes(" ")) {
        /*
         * Most likely an API error coming from the Integrates backend, this
         * condition should catch common dict KeyErrors
         */
        await window.showErrorMessage(
          `Query error. If this persists, feel free to contact us and please
          attach the extension log or a screenshot of it, which can be found
          with the Show Extension Log command`
        );
      } else {
        await window.showErrorMessage(apiError.message);
      }
  }
};

export { API_CLIENT, handleGraphQlError };
