import React from "react";

import { Lottie } from "components/Icon";
import { Tag } from "components/Tag";
import { whiteLoaderVer2 } from "resources/index";

const formatInProcessHandler = (text: string | undefined): JSX.Element => {
  return (
    <Tag variant={"grayNoBd"}>
      <Lottie animationData={whiteLoaderVer2} size={16} />
      &nbsp;
      {text}
    </Tag>
  );
};

export { formatInProcessHandler };
