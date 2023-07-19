import _ from "lodash";
import {
  window,
  // eslint-disable-next-line import/no-unresolved
} from "vscode";

interface IRetrievesLoggerAttr {
  error: (msg: string, extra?: unknown) => void;
  info: (msg: string, extra?: unknown) => void;
  warn: (msg: string, extra?: unknown) => void;
  show: () => void;
}

const retrievesOutputChannel = window.createOutputChannel("Fluid Attacks", {
  log: true,
});

const sendErrorLog = (msg: string, extra?: unknown): void => {
  retrievesOutputChannel.error(msg, _.isNil(extra) ? "" : extra);
};

const sendInfoLog = (msg: string, extra?: unknown): void => {
  retrievesOutputChannel.info(msg, _.isNil(extra) ? "" : extra);
};

const sendWarningLog = (msg: string, extra?: unknown): void => {
  retrievesOutputChannel.warn(msg, _.isNil(extra) ? "" : extra);
};

const showOutputChannel = (): void => {
  retrievesOutputChannel.show();
};

export const Logger: IRetrievesLoggerAttr = {
  error: sendErrorLog,
  info: sendInfoLog,
  show: showOutputChannel,
  warn: sendWarningLog,
};
