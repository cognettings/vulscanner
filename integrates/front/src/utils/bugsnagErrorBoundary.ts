import type { Event } from "@bugsnag/core";
import type { Error } from "@bugsnag/core/types/event";
import Bugsnag from "@bugsnag/js";
import BugsnagPluginReact from "@bugsnag/plugin-react";
import type {
  BugsnagErrorBoundary,
  BugsnagPluginReactResult,
} from "@bugsnag/plugin-react";
import _ from "lodash";
import LogRocket from "logrocket";
import React, { Fragment } from "react";

import { Logger } from "./logger";

import { getEnvironment } from "utils/environment";

const noSpaceLeftOnDevice: (error: Error) => boolean = (
  error: Error
): boolean => {
  /*
   * In this array should be added all errors related
   * to the space in the device
   */
  const expectedErrors: string[] = ["NS_ERROR_FILE_NO_DEVICE_SPACE"];

  return _.includes(expectedErrors, error.errorClass);
};

Bugsnag.start({
  apiKey: "99a64555a50340cfa856f6623c6bf35d",
  appVersion: "integrates_version",
  onError: (event: Event): boolean => {
    event.errors.forEach((error: Error): void => {
      const message: string | undefined = event.context;
      // eslint-disable-next-line fp/no-mutation
      event.context = error.errorMessage;
      // eslint-disable-next-line fp/no-mutation
      error.errorMessage = _.isString(message) ? message : "";
      // eslint-disable-next-line fp/no-mutation
      event.groupingHash = event.context;
    });
    event.addMetadata("LogRocket", {
      sessionURL: LogRocket.sessionURL,
    });
    // Custom handling to space device errors
    if (noSpaceLeftOnDevice(event.errors[0])) {
      Logger.error("noSpaceLeftOnDevice", event);

      return false;
    }

    return true;
  },
  plugins: [new BugsnagPluginReact(React)],
  releaseStage: getEnvironment(),
});

const reactPlugin: BugsnagPluginReactResult | undefined =
  Bugsnag.getPlugin("react");

const bugsnagErrorBoundary: BugsnagErrorBoundary = _.isUndefined(reactPlugin)
  ? Fragment
  : reactPlugin.createErrorBoundary(React);

export { bugsnagErrorBoundary as BugsnagErrorBoundary };
