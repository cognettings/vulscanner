import type { Error } from "@bugsnag/core/types/event";
import type Event from "@bugsnag/core/types/event";
import Bugsnag from "@bugsnag/js";

import { getEnvironment } from "utils/environment";

interface ILoggerAttr {
  error: (msg: string, extra?: unknown) => void;
  warning: (msg: string, extra?: unknown) => void;
  info: (msg: string, extra?: unknown) => void;
}

const sendBugsnagReport = (
  msg: string,
  extra: unknown,
  severity: "error" | "info" | "warning"
): void => {
  Bugsnag.notify(msg, (event: Event): void => {
    event.errors.forEach((error: Error): void => {
      // eslint-disable-next-line fp/no-mutation
      error.errorClass = `Log${severity.toUpperCase()}`;

      // eslint-disable-next-line fp/no-mutating-methods
      error.stacktrace.splice(0, 2);
    });
    event.addMetadata("extra", { extra });

    // eslint-disable-next-line fp/no-mutation
    event.severity = severity;
  });
};

const sendErrorReport = (msg: string, extra: unknown = {}): void => {
  sendBugsnagReport(msg, extra, "error");
};

const sendWarningReport = (msg: string, extra: unknown = {}): void => {
  if (getEnvironment() === "production") {
    sendBugsnagReport(msg, extra, "warning");
  }
};

const sendInfoReport = (msg: string, extra: unknown = {}): void => {
  if (getEnvironment() === "production") {
    sendBugsnagReport(msg, extra, "info");
  }
};

export const Logger: ILoggerAttr = {
  error: sendErrorReport,
  info: sendInfoReport,
  warning: sendWarningReport,
};
