/* eslint-disable fp/no-mutating-methods
  --------
  Since most Jest mocks override/mutate properties, we need to disable the above rules.
*/
import fetchMock from "fetch-mock";
import "@testing-library/jest-dom";
import failOnConsole from "jest-fail-on-console";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";

failOnConsole();

// Disable mixpanel
mixpanel.init("123");
mixpanel.disable();

// Mock fetch
Object.defineProperty(global, "fetch", { value: fetchMock, writable: true });

// Mock i18n
jest.mock(
  "react-i18next",
  (): Record<string, unknown> => ({
    ...jest.requireActual("react-i18next"),
    useTranslation: (): Record<string, unknown> => ({
      t: (key: string): string => key,
    }),
  })
);

// Mock bugsnag
jest.mock("@bugsnag/js");

// Mock idle-timer
jest.mock(
  "react-idle-timer",
  (): { useIdleTimer: () => Record<string, jest.Mock> } => ({
    useIdleTimer: (): Record<string, jest.Mock> => ({ active: jest.fn() }),
  })
);

// Set max timeout from 5000
const newMaxTime: number = 25000;
jest.setTimeout(newMaxTime);
