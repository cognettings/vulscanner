import React from "react";

import { Container } from "../../../components/Container";
import { CtaBanner } from "../../../components/CtaBanner";
import { translate } from "../../../utils/translations/translate";

const CtaSection: React.FC = (): JSX.Element => (
  <Container bgColor={"#dddde3"} ph={4} pv={5}>
    <CtaBanner
      button1Link={"https://app.fluidattacks.com/SignUp"}
      button1Text={translate.t("blog.ctaButton1")}
      button2Link={"/services/continuous-hacking/"}
      button2Text={translate.t("blog.ctaButton2")}
      image={"/airs/blogs/blogs-cta"}
      matomoAction={"Blog-free-trial"}
      paragraph={translate.t("blog.ctaDescription")}
      size={"big"}
      sizeSm={"medium"}
      title={translate.t("blog.ctaTitle")}
    />
  </Container>
);

export { CtaSection };
