import _ from "lodash";
import React from "react";

import { Tag } from "components/Tag";
import { getBgColorTech } from "utils/colors";

interface ITechnique {
  technique: string | undefined;
}

const Technique: React.FC<ITechnique> = ({
  technique,
}: ITechnique): JSX.Element => {
  const formatedTechnique: string = _.toUpper(technique);
  const currentTechniqueBgColor = getBgColorTech(_.toUpper(technique));

  return <Tag variant={currentTechniqueBgColor}>{formatedTechnique}</Tag>;
};

const techniqueFormatter = (value: string | undefined): JSX.Element => {
  return <Technique technique={value} />;
};

export type { ITechnique };
export { techniqueFormatter, Technique };
