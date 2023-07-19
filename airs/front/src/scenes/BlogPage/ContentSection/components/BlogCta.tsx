import React from "react";

import { Container } from "../../../../components/Container";
import { CtaBanner } from "../../../../components/CtaBanner";

interface IBlogCta {
  buttontxt: string;
  link: string;
  title: string;
  paragraph: string;
}

const BlogCta: React.FC<IBlogCta> = ({
  buttontxt,
  link,
  title,
  paragraph,
}): JSX.Element => (
  <Container pv={3}>
    <CtaBanner
      button1Link={link}
      button1Text={buttontxt}
      buttonClassName={"btn-rompe-trafico"}
      matomoAction={"Blog-internal-cta"}
      paragraph={paragraph}
      pv={4}
      size={"xs"}
      textSize={"medium"}
      title={title}
      variant={"dark"}
    />
  </Container>
);

export { BlogCta };
