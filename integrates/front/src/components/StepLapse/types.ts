import type { ReactNode } from "react";

interface IStep {
  content: ReactNode;
  isDisabledNext?: boolean;
  isDisabledPrevious?: boolean;
  nextAction?: () => void;
  previousAction?: () => void;
  title: string;
}

interface IStepLapseProps {
  finalButtonText: string;
  finalButtonType?: "button" | "reset" | "submit";
  finalClick?: () => void;
  isDisabledFinalButton?: boolean;
  steps: IStep[];
}

export type { IStepLapseProps };
