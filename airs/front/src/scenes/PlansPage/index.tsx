import React from "react";

import { ComparativePlans } from "./Comparative";
import { PlansFaq } from "./FaqSection";
import { Header } from "./Header";
import { PlansCta } from "./PlansCta";

const PlansPage: React.FC = (): JSX.Element => {
  return (
    <React.Fragment>
      <Header />
      <ComparativePlans />
      <PlansFaq />
      <PlansCta />
    </React.Fragment>
  );
};

export { PlansPage };
