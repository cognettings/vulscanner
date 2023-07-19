import React, { useEffect } from "react";

import { BigScreenSignUp } from "./big-screen";
import { SmallScreenSignUp } from "./small-screen";

import { useWindowSize } from "hooks";

export const SignUp: React.FC = (): JSX.Element => {
  const { width } = useWindowSize();

  useEffect((): VoidFunction => {
    sessionStorage.setItem("trial", "true");

    return (): void => {
      sessionStorage.removeItem("trial");
    };
  }, []);

  if (width < 940) {
    return <SmallScreenSignUp />;
  }

  return <BigScreenSignUp />;
};
