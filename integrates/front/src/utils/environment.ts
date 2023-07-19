import _ from "lodash";

type Environment = "development" | "ephemeral" | "production";

export const getEnvironment: () => Environment = (): Environment => {
  if (_.isUndefined(window)) {
    return "development";
  }
  const currentUrl: string = window.location.hostname;
  const ephemeralDomainRegex: RegExp = /[a-z]+atfluid.app.fluidattacks.com/gu;

  if (currentUrl === "localhost") {
    return "development";
  } else if (ephemeralDomainRegex.test(currentUrl)) {
    return "ephemeral";
  }

  return "production";
};
