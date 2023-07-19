import React from "react";
import { useWindowSize } from "usehooks-ts";

import { ContinuousHackingClientsDesktop } from "./Desktop";
import { ContinuousHackingClientsMobile } from "./Mobile";

const ContinuousHackingClients: React.FC = (): JSX.Element => {
  const { width } = useWindowSize();

  if (width > 960) {
    return <ContinuousHackingClientsDesktop />;
  }

  return <ContinuousHackingClientsMobile />;
};

export { ContinuousHackingClients };
