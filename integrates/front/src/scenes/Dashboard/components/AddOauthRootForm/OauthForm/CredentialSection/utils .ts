import type { ICredentialsAttr } from "../../types";

const getCredentials = (
  credentials: ICredentialsAttr[],
  provider: string
): ICredentialsAttr[] => {
  return credentials.filter(
    (credential: ICredentialsAttr): boolean =>
      credential.type === "OAUTH" && credential.oauthType === provider
  );
};

export { getCredentials };
