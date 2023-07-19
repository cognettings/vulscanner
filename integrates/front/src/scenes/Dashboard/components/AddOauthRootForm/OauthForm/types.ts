import type { IIntegrationRepository, Provider } from "../types";

interface IOauthFormProps {
  trialOrgId?: string;
  provider?: Provider;
  setIsCredentialSelected?: React.Dispatch<React.SetStateAction<boolean>>;
  setProgress?: React.Dispatch<React.SetStateAction<number>>;
  setRepos: React.Dispatch<
    React.SetStateAction<Record<string, IIntegrationRepository>>
  >;
}

export type { IOauthFormProps };
