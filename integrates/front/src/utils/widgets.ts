// Third party embeddable scripts not designed for SPAs

import { Logger } from "./logger";

// https://app.delighted.com/docs/api/web#full-api-reference
interface IDelighted {
  delighted?: {
    survey: (options: { email: string; name: string }) => void;
  };
}

const initializeDelighted = (userEmail: string, userName: string): void => {
  const { delighted } = window as IDelighted & typeof window;

  if (delighted) {
    if (!userEmail.endsWith("@fluidattacks.com")) {
      delighted.survey({ email: userEmail, name: userName });
    }
  } else {
    Logger.warning("Couldn't initialize delighted");
  }
};

interface IZendesk {
  zE: (action: string, event: string, parameters?: unknown) => void;
}

const showZendesk = (): void => {
  const { zE } = window as IZendesk & typeof window;
  zE("webWidget", "show");
};

const hideZendesk = (): void => {
  const { zE } = window as IZendesk & typeof window;
  zE("webWidget", "hide");
};

const initializeZendesk = (userEmail: string, userName: string): void => {
  const { zE } = window as IZendesk & typeof window;
  try {
    zE("webWidget", "updateSettings", {
      webWidget: { navigation: { popoutButton: { enabled: false } } },
    });
    zE("webWidget", "hide");
    zE("webWidget:on", "open", showZendesk);
    zE("webWidget:on", "close", hideZendesk);
    zE("webWidget", "setLocale", "en-US");
    zE("webWidget", "identify", { email: userEmail, name: userName });
    zE("webWidget", "prefill", {
      email: { value: userEmail },
      name: { value: userName },
    });
  } catch (exception: unknown) {
    Logger.warning("Zendesk widget failed to load", exception);
  }
};

const toggleZendesk = (): void => {
  const { zE } = window as IZendesk & typeof window;
  zE("webWidget", "toggle");
};

export { initializeDelighted, initializeZendesk, toggleZendesk };
