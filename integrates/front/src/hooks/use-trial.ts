import { useQuery } from "@apollo/client";

import { GET_STAKEHOLDER_TRIAL } from "./queries";

import { getTrialRemainingDays } from "utils/getTrialRemainingDays";
import { Logger } from "utils/logger";

interface ITrial {
  completed: boolean;
  extensionDate: string;
  extensionDays: number;
  startDate: string;
  state: "EXTENDED_END" | "EXTENDED" | "TRIAL_ENDED" | "TRIAL";
}

interface IMeData {
  me: {
    userEmail: string;
    trial: ITrial | null;
  };
}

const useTrial = (): {
  remainingDays: number;
  trial: ITrial;
} | null => {
  const { data } = useQuery<IMeData>(GET_STAKEHOLDER_TRIAL, {
    onError: (error): void => {
      error.graphQLErrors.forEach(({ message }): void => {
        Logger.error("An error occurred loading trial", message);
      });
    },
  });

  if (data === undefined) {
    return null;
  }

  const { trial } = data.me;

  if (trial === null) {
    return null;
  }

  const remainingDays = getTrialRemainingDays(trial);

  return { remainingDays, trial };
};

export { useTrial };
