import { getDatePlusDeltaDays, getRemainingDays } from "utils/date";

interface ITrialData {
  completed: boolean;
  extensionDate: string;
  extensionDays: number;
  startDate: string;
  state: "EXTENDED_END" | "EXTENDED" | "TRIAL_ENDED" | "TRIAL";
}

const getTrialRemainingDays = (trial: ITrialData): number => {
  if (trial.state === "TRIAL" && trial.startDate) {
    const TRIAL_DAYS = 21;

    return getRemainingDays(getDatePlusDeltaDays(trial.startDate, TRIAL_DAYS));
  }
  if (trial.state === "EXTENDED" && trial.extensionDate) {
    return getRemainingDays(
      getDatePlusDeltaDays(trial.extensionDate, trial.extensionDays)
    );
  }

  return 0;
};

export { getTrialRemainingDays };
