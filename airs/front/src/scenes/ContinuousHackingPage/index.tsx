import React from "react";

import { ContinuousHackingClients } from "./Clients";
import { DiscoverContinuousHacking } from "./Discover";
import { ContinuousHackingPlans } from "./Plans";
import { ContinuousHackingHeader } from "./Portrait";
import { ContinuousHackingTools } from "./Tools";

const ContinuousHackingPage: React.FC = (): JSX.Element => {
  return (
    <React.Fragment>
      <ContinuousHackingHeader />
      <DiscoverContinuousHacking />
      <ContinuousHackingTools />
      <ContinuousHackingPlans />
      <ContinuousHackingClients />
    </React.Fragment>
  );
};

export { ContinuousHackingPage };
