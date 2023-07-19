import type React from "react";
import { createContext, useContext } from "react";

interface IMeetingModeContext {
  meetingMode: boolean;
  setMeetingMode?: React.Dispatch<React.SetStateAction<boolean>>;
}

const meetingModeContext = createContext<IMeetingModeContext>({
  meetingMode: false,
});

interface IMeetingModeProps {
  children: JSX.Element;
}

const MeetingMode: React.FC<IMeetingModeProps> = ({
  children,
}): React.ReactElement | null => {
  const { meetingMode } = useContext(meetingModeContext);

  if (meetingMode) {
    return children;
  }

  return null;
};

export type { IMeetingModeContext };
export { MeetingMode, meetingModeContext };
