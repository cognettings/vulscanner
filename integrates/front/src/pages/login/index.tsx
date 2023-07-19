import React from "react";

import { BigScreenLogin } from "./big-screen";
import { SmallScreenLogin } from "./small-screen";

import { useWindowSize } from "hooks";

export const Login: React.FC = (): JSX.Element => {
  const { width } = useWindowSize();

  if (width < 940) {
    return <SmallScreenLogin />;
  }

  return <BigScreenLogin />;
};
