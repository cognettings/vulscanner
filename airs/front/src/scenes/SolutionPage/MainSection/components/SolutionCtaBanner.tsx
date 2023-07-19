import React from "react";

import { Container } from "../../../../components/Container";
import { CtaBanner } from "../../../../components/CtaBanner";
import type { ICtaBannerProps } from "../../../../components/CtaBanner/types";
import { translate } from "../../../../utils/translations/translate";

const SolutionCtaBanner: React.FC<ICtaBannerProps> = ({
  paragraph,
  title,
}): JSX.Element => (
  <Container bgColor={"#fff"} ph={4} pv={5}>
    <CtaBanner
      button1Link={"https://app.fluidattacks.com/SignUp"}
      button1Text={translate.t("blog.ctaButton1")}
      button2Link={"/contact-us/"}
      button2Text={translate.t("blog.ctaButton2")}
      matomoAction={"Solution-free-trial"}
      paragraph={paragraph}
      size={"big"}
      sizeSm={"small"}
      title={title}
    />
  </Container>
);

export { SolutionCtaBanner };
