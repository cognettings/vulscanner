import type { ICredentialsAttr } from "./types";

interface IAvailableProviders {
  azure: boolean;
  bitbucket: boolean;
  gitHub: boolean;
  gitLab: boolean;
}

const isAvailable = (
  credentials: ICredentialsAttr[],
  provider: string
): boolean => {
  return (
    credentials.filter(
      (credential: ICredentialsAttr): boolean =>
        credential.type === "OAUTH" && credential.oauthType === provider
    ).length >= 1
  );
};

const showProviders = (
  credentials: ICredentialsAttr[]
): IAvailableProviders => {
  return {
    azure: isAvailable(credentials, "AZURE"),
    bitbucket: isAvailable(credentials, "BITBUCKET"),
    gitHub: isAvailable(credentials, "GITHUB"),
    gitLab: isAvailable(credentials, "GITLAB"),
  };
};

export { showProviders };
