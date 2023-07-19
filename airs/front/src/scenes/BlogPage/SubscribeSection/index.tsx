import React from "react";

import { Container } from "../../../components/Container";
import { CtaBanner } from "../../../components/CtaBanner";
import { translate } from "../../../utils/translations/translate";

const SubscribeSection: React.FC = (): JSX.Element => {
  return (
    <Container ph={4} pv={5}>
      <Container center={true} maxWidth={"1000px"}>
        <CtaBanner
          button1Link={"/subscription/"}
          button1Text={translate.t("blog.subscribeCta.button")}
          matomoAction={"blog-internal-subscribe"}
          paragraph={translate.t("blog.subscribeCta.paragraph")}
          sizeMd={"medium"}
          title={translate.t("blog.subscribeCta.title")}
        />
      </Container>
    </Container>
  );
};

export { SubscribeSection };
